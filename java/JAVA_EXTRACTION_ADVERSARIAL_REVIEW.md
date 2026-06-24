# JAVA_EXTRACTION_ADVERSARIAL_REVIEW

**Adversarial attack on the extraction (lxml) blocker proof. Every candidate JVM HTML parser and
bridge is evaluated against the project's byte-exact + pure-Java + cross-platform-deterministic
constraints.** Python canon `9625f4a`.

## Question
Can byte-exact parity with Python `extract()` (which parses via `BeautifulSoup(text, "lxml")` =
libxml2's `htmlParseDocument` recovery mode) be achieved **under project constraints**? — **NO.**

## The bar (project constraints)
1. **Byte-exact**: `stable_serialize`/`compute_kaalka_hash` identical to Python on arbitrary input
   (incl. the global `fingerprint` computed over `content.text`/`content.links`/`raw_text`).
2. **Pure Java / Maven-Central**: no native binaries, no external runtime, no per-platform artifacts.
3. **Cross-platform deterministic**: identical output on win/mac/linux × arch, independent of any
   installed system library version.

## Discriminating test vectors (empirically established)
| Input | libxml2 (Python lxml) | WHATWG HTML5 / `html.parser` |
|-------|-----------------------|------------------------------|
| `<a href="first" href="second">x</a>` | `href = "first"` (**first wins**) | `href = "second"` (**last wins**) |
| `<!-- c --><div>v<![CDATA[x]]></div>` | text = `"v"` (CDATA dropped) | text = `"v x"` (CDATA surfaced) |
Both reach `content.text`/`content.links`/`raw_text` and cascade to the 317 KB `fingerprint`.

## Candidate-by-candidate

### jsoup — NO
Implements the **WHATWG HTML5** tree-construction algorithm. HTML5 mandates **last-wins** duplicate
attributes (→ `"second"`) and parses `<![CDATA[…]]>` in HTML content per foreign-content/bogus-comment
rules — both diverge from libxml2 (proven above). jsoup's adoption-agency misnesting recovery also
differs from libxml2's. Cannot match libxml2 byte-exact.

### NekoHTML — NO
A Xerces-based HTML scanner with its *own* error-correction (tag balancing, implied tags) tuned to
Xerces/XNI, not libxml2. Different recovery heuristics ⇒ different text-node order and element tree on
malformed input. No libxml2 equivalence; also effectively unmaintained.

### TagSoup — NO
A SAX parser using its own (Hauser) tag-rebalancing rules and a fixed HTML schema. Its recovery model
is neither HTML5 nor libxml2; it diverges on misnesting, implied elements, and CDATA. Not byte-exact.

### HTML5 parser (validator.nu / any spec-compliant) — NO
By definition implements the WHATWG algorithm. libxml2 is **not** an HTML5 parser — it is libxml2's own
HTML4-era recovery (`htmlParseDocument`). A spec-correct HTML5 parser is therefore *guaranteed* to
diverge from libxml2 on exactly the cases above (last-wins attrs, CDATA, adoption agency). NO.

### libxml2 via JNI — NO (constraint violation)
A JNI binding to native libxml2 *would* match its behavior — but: (a) ships **per-platform/per-arch
native binaries**, breaking the pure-Java / Maven-Central contract; (b) re-introduces a **version-skew
non-determinism** (libxml2 2.9 vs 2.12 differ in recovery), violating cross-platform determinism;
(c) adds a native attack/operability surface. It cannot be *guaranteed* byte-exact and portable across
the supported matrix. Fails constraints 2 and 3.

### Subprocess bridge (shell out to Python/libxml2) — NO (constraint violation)
Requires a Python + libxml2 runtime present and identical on every host — an external runtime
dependency that is non-portable, non-deterministic across environments, and defeats the purpose of an
independent Java port (parity would be "Python calling Python"). Fails constraints 2 and 3 outright.

## Frontier-reduction re-test
`extract()`'s observable fields are `soup.get_text(" ")`, `find_all("a")` hrefs, and `title.string` —
each a pure function of the libxml2 recovery tree over arbitrary (often malformed) HTML. There is no
discardable intermediate (unlike S22's epistemic engine); the minimal observable frontier *is* the full
libxml2 parse. No reduction exists.

## Verdict
**NO** — byte-exact parity for the lxml extraction family cannot be achieved under project constraints.
Every spec-correct or independent JVM parser (jsoup/NekoHTML/TagSoup/HTML5) diverges from libxml2 on
demonstrable inputs; the only behaviorally-matching options (libxml2 JNI / subprocess) violate the
pure-Java, cross-platform-deterministic constraints. The blocker stands. Unblock requires an **upstream
canon change** (replace `BeautifulSoup(text,"lxml")` in `safe_parser`+`html_extractor` with a
specified, portable parser). Affected: `extract`, `extract_async`, `extract_docs`, `extract_repo`,
`stream_extract`, `analyze` (default branch), `extract_recursive`, and the aggregator
`run_canonical_pipeline` (inherits).
