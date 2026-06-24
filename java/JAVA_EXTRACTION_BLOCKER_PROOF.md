# JAVA_EXTRACTION_BLOCKER_PROOF

**Tier-C extraction-family substrate audit (Session 27). Verdict: CASE B — formal blocker proof
for all six APIs. No common portable parser contract exists; the family is byte-exact-blocked under
current canon.** Python canon `9625f4a`. Method: runtime call graph + observable-output tracing +
discarded-field analysis + empirical execution (bs4 4.14.3 / lxml 6.1.1, Python 3.11).

---

## 0. Executive verdict

The Session-27 hypothesis was: *"does the extraction family share a common observable parser
contract that can be ported?"* **It does not.** Tracing the runtime call graph (not import closure)
falsifies the premise: the six target APIs decompose into **three disjoint substrates**, only one of
which is a parser at all:

| Substrate | APIs | Blocker | Class |
|-----------|------|---------|-------|
| **L — lxml HTML parser** (`BeautifulSoup(text, "lxml")`) | `extract`, `extract_docs`, `stream_extract` | byte-exact libxml2 tree-building reaches observable output (PROVEN below) | CASE B |
| **N — network + regex** (`requests`/`httpx` + `re.findall`) | `crawl`, `crawl_async` | live HTTP I/O; not a deterministic function; **no parser** | network-bound |
| **P — Playwright** (`render_page` → `page.content()`) | `extract_web` | live headless-Chromium render; **no lxml**; html.parser engines run only on a live page | platform-bound |

There is therefore no single "Soup engine" that unlocks the family. The prior memory tag
("extraction-lxml 6 → Tier-C Soup engine") conflated three substrates; the runtime audit corrects it.
Each substrate is independently blocked. **Port path exists for none of the six under current canon.**

---

## SUBSTRATE L — `extract` / `extract_docs` / `stream_extract` (CASE B, lxml)

### L.1 Runtime call graph (the complete lxml frontier)

```
extract(input) / extract_docs(src)=extract(src) / stream_extract(t)=extract(t)+chunk metadata
└ _extract_core(text, source_url)                          core/extract/pipeline.py
  ├ safe_html_text(safe_text)        ── BeautifulSoup(text, "lxml"); decompose script/style; get_text(" ")
  │     → merged["raw_text"]                                ← OBSERVABLE
  ├ extract_html(safe_text)          ── BeautifulSoup(text, "lxml")
  │     → content.text  = soup.get_text(separator=" ", strip=True)        ← OBSERVABLE
  │     → content.links = sorted({a.get("href") for a in find_all("a")})  ← OBSERVABLE
  │     → code.blocks   = sorted(get_text of pre/code)                     ← OBSERVABLE
  │     → metadata.title= soup.title.string                               ← OBSERVABLE
  ├ extract_markdown / code / dependencies / architecture / metadata /
  │ repository_data / repository_intelligence / *_v2 / analyze_document /
  │ analyze_repository                                       ── all pure regex/text; NO parser
  ├ normalize_output(merged) ; enrich_extraction(...)        ── pure; preserve the lxml fields
  └ compute_global_runtime_fingerprint(...)  → fingerprint   ← OBSERVABLE (317 KB identity hash)
```

**Empirically verified the frontier is exactly two functions.** A repo-wide grep for parser
constructors shows only `core/extract/html_extractor.py:7` and `core/security/safe_parser.py:8` use
`"lxml"`; every other `BeautifulSoup` in the codebase uses `"html.parser"` and none of those modules
are imported by `_extract_core`. Monkeypatching **only** `safe_parser.BeautifulSoup` and
`html_extractor.BeautifulSoup` to `html.parser` and re-running full `extract()` produces a closed,
complete set of diverging fields (§L.3) — confirming these two are the entire lxml surface.

### L.2 Concrete examples — lxml vs html.parser at the engine

Two minimal inputs, run through the real `safe_html_text` / `extract_html` bodies:

```
input: <!-- c --><div>v<![CDATA[x]]></div><a href="c">cl</a>
  safe_html_text  lxml="v cl"        html.parser="v x cl"      (lxml drops CDATA text)
  content.text    lxml="v cl"        html.parser="v x cl"

input: <a href="first" href="second">dup</a>
  content.links   lxml=["first"]     html.parser=["second"]    (duplicate-attr resolution differs)
```

These are not exotic: CDATA sections and duplicate attributes occur in real-world tag soup. lxml
(libxml2 HTML recovery mode) keeps the **first** duplicate attribute and discards bogus CDATA text;
Python's `html.parser` keeps the **last** attribute and surfaces CDATA as text. (jsoup, the only
mature JVM HTML parser, implements the WHATWG HTML5 algorithm — a *third* tree-builder that agrees
with neither: HTML5 keeps the **last** duplicate attribute and parses CDATA per foreign-content
rules. So no off-the-shelf JVM parser matches libxml2.)

### L.3 Discarded-field analysis — the divergence SURVIVES to the serialized output

Full `extract()` run, lxml vs (both touchpoints forced to) html.parser, JSON-flattened and diffed:

```
comment_cdata → 8 observable fields differ:
   content.text                                       'v cl'   vs 'v x cl'
   raw_text                                           'v cl'   vs 'v x cl'
   fingerprint                                        <317106 ch>  ≠  <317114 ch>
   metadata.observability_v18…raw_text_bytes          4  vs 6
   metadata.quality_v17.extraction.score              0.0008 vs 0.0012
   metadata.quality_v18.ranked_extractions[0].raw_text_len  4 vs 6
   metadata.serialization_v4.canonical_length         158459 vs 158463
   metadata.serialization_v5.canonical_length         158459 vs 158463

duplicate_attr → 4 observable fields differ:
   content.links[0]                                   'first'  vs 'second'
   fingerprint                                        <316782 ch>  ≠  <316784 ch>
   metadata.serialization_v4.canonical_length         158297 vs 158298
   metadata.serialization_v5.canonical_length         158297 vs 158298
```

The lxml output is **not** an intermediate that gets discarded. `content.text`/`content.links`/
`raw_text` are top-level result fields; they further feed `compute_global_runtime_fingerprint`, which
emits the 317 KB `fingerprint` — the canonical deterministic identity of the whole result and a field
every parity vector embeds. **Any** parity vector built from `extract()` output therefore fails
byte-exact if the parser diverges on the input.

### L.4 Why frontier reduction fails

Reduction worked for prior wins (e.g. S22 `query_documents`) because the expensive engine's output
was **computed then discarded** — the observable surface didn't depend on it. Here the opposite holds:
the observable surface (`get_text`, `find_all("a")`, `title.string`) **is** a pure function of the
lxml parse tree. For arbitrary/malformed HTML, the text-node order, whitespace coalescing, which
content survives (CDATA, comments, misnested recovery, implied tags), and attribute-collision
resolution are all decided by libxml2's recovery tree-builder. You cannot regex your way to lxml's
`get_text()` on arbitrary input — there is no smaller observable frontier than "the full libxml2
tree." This is structurally identical to the AST blocker (§JAVA_AST_FRONTIER_*): the parser output
**is** the answer, so there is no discard to exploit.

### L.5 Why byte-exact parity cannot be guaranteed

Matching `extract()` byte-exact for all inputs requires reproducing libxml2's `htmlParseDocument`
recovery semantics in Java: its CDATA/comment/PI handling, first-wins duplicate-attribute rule, tag
soup recovery and implied-tag insertion, entity tables, and text coalescing. No JVM library does
this — `html.parser` parity (which the Dart branch built) is the **wrong** target (proven divergent
in §L.2/L.3), and jsoup's HTML5 tree-builder is a third, also-divergent algorithm. Reproducing
libxml2 byte-exact = porting libxml2's HTML parser into the JVM, a non-portable native-equivalent
dependency. **Success-condition B.** `extract_docs` is `return extract(src)` and `stream_extract`
embeds the full `extract()` output (plus pure chunk metadata), so both inherit the identical blocker.

---

## SUBSTRATE N — `crawl` / `crawl_async` (network-bound; NOT a parser blocker)

### N.1 Runtime call graph

```
crawl(url) = core.crawling.crawler_engine.crawl          (public crawl/_crawl)
crawl_async(url) = asyncio.to_thread(_crawl, url)        ← identical observable output, async shell
  └ DeterministicQueue / CrawlBudget / canonical_url / allow_url   ── pure
  └ fetch_sync(url)  ── requests.get(...)                ← LIVE HTTP I/O
  └ discover_links(base, text)  ── re.findall(r'href=["\']([^"\']+)["\']', …) + markdown re  ── PURE REGEX
  → {visited, queued, discovered, depth_map}             ← all URL lists
```

**Empirically confirmed bs4/lxml-free:** importing the entire `core.crawling` closure leaves
`sys.modules` with no `bs4`/`lxml`. Link discovery is pure regex — fully portable.

### N.2 Why blocked

The sole obstruction is `fetch_sync` → `requests.get` (live HTTP). The observable output is a
deterministic function of the **fetched bytes**, but those bytes come from the live network:

```
crawl("http://nonexistent.invalid.localhost.test/seed", max_depth=1)
  → {visited:[seed], queued:[], discovered:[], depth_map:{seed:0}}   (deterministic ONLY because the fetch failed)
```

A reachable URL returns content-dependent, time-varying results; offline the API degrades to the
empty-discovery case. There is no parser to port and no byte-exact-impossible computation — but there
is also no way to **certify** parity without real, pinned network responses, which the parity harness
does not provide. Classification: **network-bound**, the same tier as the live-page APIs
(`run_live_runtime`, `capture_websocket_frames`). Portable the moment canon adds a fetch-injection /
fixture contract; not certifiable as a pure function today.

---

## SUBSTRATE P — `extract_web` (platform-bound; NOT lxml)

### P.1 Runtime call graph

```
extract_web(url, …) = core.browser.universal_web_extraction_engine.extract_web
  └ render_page(url, …)                                  core/browser/playwright_runtime.py
      if sync_playwright is None: return {available:False, reason:"playwright_missing", bounded:True}
      else: chromium.launch(headless=True); page.goto(url, wait_until="networkidle"); html=page.content()
  └ if not runtime["available"]:  return {**runtime, url, session, authenticated, bounded}   ← bail-out
  └ (only with a live page) reconstruct_dom(html), extract_semantic_content(html)  ── "html.parser", NOT lxml
```

### P.2 Why blocked

`extract_web` is fundamentally a Playwright API. Without a browser it returns the deterministic
bail-out `{available:False, reason:"playwright_missing", url, session, authenticated:False, bounded}`.
With a browser, the entire payload derives from `page.content()` — live headless-Chromium rendering
after `networkidle` — which is non-deterministic and platform-coupled. The HTML parsing it does use
(`reconstruct_dom`, `extract_semantic_content`) is `"html.parser"`, runs **only** on a live page, and
is never reached offline. **No lxml involvement; platform-bound** (Tier-4), the same class as the
other `page`-driven APIs. Not part of the extraction-parser substrate at all.

---

## Per-API classification (success condition met — no "unknown")

| API | Substrate | Verdict | Obstruction |
|-----|-----------|---------|-------------|
| `extract` | L | **CASE B blocked** | libxml2 byte-exact tree-building reaches `content.*`/`raw_text`/`fingerprint` |
| `extract_docs` | L | **CASE B blocked** | `return extract(src)` — inherits L |
| `stream_extract` | L | **CASE B blocked** | embeds full `extract()` output (+ pure chunk metadata) — inherits L |
| `crawl` | N | network-bound | live `requests.get`; regex discovery is portable, fetch is not certifiable offline |
| `crawl_async` | N | network-bound | `asyncio.to_thread(_crawl)` — identical to `crawl` |
| `extract_web` | P | platform-bound | Playwright `page.content()`; no lxml |

## What would unblock each (canon-change levers, not in-scope this session)

- **L:** replace `BeautifulSoup(text,"lxml")` with a portable/specified parser in `safe_parser` +
  `html_extractor` (upstream Python canon change), OR embed a libxml2-equivalent HTML recovery
  tree-builder in Java (non-portable). Until then: blocked.
- **N:** add a deterministic fetch-injection/fixture contract to `crawl` so parity vectors can pin
  responses. The regex link engine itself is already portable.
- **P:** add a Playwright-free deterministic contract (e.g. accept an `html=` snapshot like
  `run_application_cognition` did) — currently absent for `extract_web`.

## Bottom line

The extraction family does **not** share a common portable parser contract. Substrate L
(`extract`/`extract_docs`/`stream_extract`) is a formal **CASE B** byte-exact blocker on libxml2;
substrates N and P are network/platform-bound and parser-irrelevant. **No port path exists for any of
the six under current canon.** State unchanged at 97/128; the extraction family is now closed with
proof rather than left "unknown."
