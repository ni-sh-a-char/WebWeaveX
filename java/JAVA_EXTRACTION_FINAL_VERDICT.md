# JAVA_EXTRACTION_FINAL_VERDICT

**Phase-2 re-audit (Session 28). The Session-27 blocker was challenged with jsoup, tag-soup, HTML5,
libxml2-embedding and JNI. It survives.** Python canon `9625f4a`. See JAVA_EXTRACTION_BLOCKER_PROOF.md
for the full empirical substrate trace; this file is the adversarial re-test demanded by the directive.

## Family split (re-confirmed by runtime call graph)
| API | Substrate | Verdict |
|-----|-----------|---------|
| `extract`, `extract_async`, `extract_docs`, `extract_repo`, `stream_extract` | lxml | **CASE B blocked** |
| `analyze` (default branch), `extract_recursive` | lxml (via `extract`) | **CASE B blocked** |
| `crawl`, `crawl_async` | network + regex | network-bound (no parser) |
| `extract_web` | Playwright live render | platform-bound (see JAVA_PLAYWRIGHT_VERDICT) |

`analyze(input, edges=None)`: the `edges`-given branch is pure (`analyze_graph`), but the default
branch is `extract(input)` → lxml. `extract_recursive` = `crawl` + `extract`. Both inherit CASE B.

## Challenge: can lxml parity be reproduced byte-exact in the JVM?

### A. Concrete divergences (observable, survive to fingerprint)
```
<!-- c --><div>v<![CDATA[x]]></div><a href="c">cl</a>
   lxml content.text = "v cl"      html.parser/jsoup(HTML5) = "v x cl"   (CDATA handling)
<a href="first" href="second">dup</a>
   lxml content.links = ["first"]  html.parser = ["second"]  jsoup(HTML5) = ["second"]  (dup-attr)
```
Full-pipeline diff (lxml vs html.parser) cascades to `content.text`/`content.links`/`raw_text` + the
317 KB global `fingerprint` + `quality_v17/18` + `serialization_v4/5` canonical lengths.

### B. The three candidate parsers all disagree with libxml2
- **jsoup** implements the **WHATWG HTML5** tree-builder: keeps the **last** duplicate attribute,
  parses CDATA per foreign-content rules, and applies HTML5 adoption-agency misnesting recovery —
  none byte-identical to libxml2's `htmlParseDocument` recovery mode.
- **Python `html.parser`** (what the Dart branch certified) is a *third* algorithm — proven divergent
  in §A. Reusing a Dart-style html.parser-parity engine would **not** match Python `extract()`.
- **A hand "tag-soup" parser** would have to re-derive libxml2's exact recovery heuristics (implied
  tags, text coalescing, entity tables, CDATA/comment/PI handling, first-wins attributes) — i.e.
  re-implement libxml2.

### C. libxml2 embedding / JNI — rejected under project constraints
A JNI binding to native libxml2 would (1) break the pure-Java / Maven-Central portability contract,
(2) require per-platform native binaries (win/mac/linux × arch), and (3) re-introduce a
cross-platform determinism risk (libxml2 version skew changes recovery output). The parity contract
requires deterministic, dependency-free Java; a native binding is explicitly non-portable. So even
though libxml2 *could* be invoked, it cannot be **guaranteed** byte-exact and portable across the
supported matrix — failing the certification bar.

### D. Frontier reduction fails
`get_text()`/`find_all("a")`/`title.string` are pure functions of the libxml2 recovery tree; for
arbitrary malformed HTML the text-node order, surviving content, and attribute resolution are all
decided by that tree. There is no smaller observable frontier than "the full libxml2 parse," and no
discard to exploit (unlike S22). 

## crawl / crawl_async (network-bound, not a parser blocker)
`discover_links` is pure regex (bs4/lxml-free — verified: importing `core.crawling` leaves no
`bs4`/`lxml` in `sys.modules`). The sole obstruction is live `requests.get`/`httpx`: output is a
deterministic function of fetched bytes, but those bytes are non-deterministic / unavailable offline,
and parity vectors cannot pin them without a fetch-fixture contract. Classification: **network-bound**
(same tier as live-page APIs), portable the moment canon adds a fetch-injection contract.

## Verdict
**Extraction family closed.** lxml substrate (7 APIs incl. `analyze`/`extract_recursive`) = formal
**CASE B** blocker; `crawl`/`crawl_async` = network-bound; `extract_web` = platform-bound. No port
path under current canon. Unblock levers: replace lxml in `safe_parser`+`html_extractor` upstream
(L), add fetch-fixture contract (N), add `html=` snapshot contract for `extract_web` (P).
