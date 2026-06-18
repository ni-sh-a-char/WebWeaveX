# JAVA_SESSION_4A_EXECUTION_PLAN

**Phase 8 execution plan + Phase 6 test strategy + Phase 4 detailed feasibility.**

This is the concrete, ordered plan the *next* (implementation) session executes. This 4A
session is **analysis only** and writes no Java, no vectors, no governance changes. Every
step below cites the policy/validator hook it satisfies.

---

## Part A — Feasibility ledger (Phase 4)

Verdict key: **READY** = pure, JDK-only, byte-exact provable now · **READY-H** = deterministic
but needs a declared canonicalization harness · **BLOCKED-S** = needs a Soup engine ·
**BLOCKED-N** = network/browser at boundary (not stub-free certifiable) · **DEFERRED** =
binary-parser / `sys.platform` (permanent).

| API | Verdict | Self-contained? | Why |
| --- | --- | --- | --- |
| `extract_document_runtime` | **READY** | Yes (8 pure engines) | text→IR, no hash, no I/O |
| `extract_paginated_content` | **READY** | Yes | fixture-page traversal |
| `heal_selector` | **READY** (html-arg scoped) | Yes (Risk R-7) | pure selector logic |
| `ingest_input` | **READY** | Yes | extension-map dispatch |
| `extract_archive` *(internal)* | **READY** | Yes | stdlib `zipfile` |
| `analyze_document` *(internal)* | **READY** | Yes | 3 pure text engines |
| `compile_media_ir` *(internal)* | **READY** | Yes | trivial wrapper |
| `compile_document` | **READY** (large) | Yes (~20 pure engines) | epistemic IR, no hash |
| `run_live_runtime` | **READY** | Yes (connectors DONE) | pure aggregation |
| `extract_repository` | **READY-H** | Yes (11 engines) | abs-path/separator (R-2) |
| `run_autonomous_extraction` (core) | **READY** (core) | Yes | pure scheduler; native fan-out deferred |
| `replay_interactions` (output) | **READY** (output) | Yes | deterministic replay log |
| `extract`/`extract_async`/`extract_docs`/`extract_repo` | **BLOCKED-S** (lxml) | No (L1b+L3a) | `_extract_core` bs4/lxml + fingerprint stack |
| `stream_extract` | **BLOCKED-S** (lxml) | No | transitive `extract()` |
| `analyze` (source-mode) | **BLOCKED-S** | No | via `extract` |
| `extract_html_file`/`universal_extract`(html) | **BLOCKED-S** (html.parser) | No (L3b) | bs4/html.parser ×3 |
| `extract_web` | **BLOCKED-N** | No | Playwright + html.parser |
| `crawl`/`crawl_async`/`extract_recursive` | **BLOCKED-N** | No | `fetch_sync` network |
| `extract_infinite_scroll`/`capture_dom_mutations`/`capture_websocket_frames` | **BLOCKED-N** (source); transform READY-fixture | partial | live browser source |
| `extract_native`/`run_native_cognition` | **DEFERRED** | n/a | `sys.platform` |
| internal `extract_pdf_text`/`extract_docx_text`/OCR | **DEFERRED** | n/a | pypdf/python-docx/Tesseract |

**Decision: the next implementation slice (call it 4B) ships the READY Class-A family**
(`extract_document_runtime`, `extract_paginated_content`, `heal_selector`, `ingest_input`),
raising Java proven APIs **21 → 25**. `compile_document`, `extract_repository`,
`run_live_runtime` follow as their own slices (4C/4D/4E). The Soup-gated Class C is a
separate multi-session program (4F+).

---

## Part B — Exact implementation order (Phase 8.1)

**Slice 4B (recommended next; no new substrate):**
1. `io.webweavex.documents.DocumentRuntime` ← `extract_document_runtime`
   - sub-engines ported as package-private helpers: `DocumentStructure`, `DocumentHierarchy`,
     `Citations`, `References`, `DocumentTables`, `DocumentKnowledgeGraph`,
     `PresentationStructure`, `SpreadsheetStructure`, `DocumentRuntimeIr`.
2. `io.webweavex.interaction.Pagination` ← `extract_paginated_content` (define a Java
   `PageView` interface mirroring the `_test_url`/`_test_paginate`/`click` fixture contract).
3. `io.webweavex.adaptive.SelectorHealing` ← `heal_selector` (+ `SemanticAnchor` with the
   html argument scoped empty/trivial per R-7).
4. `io.webweavex.ingestion.Ingestion` ← `ingest_input` (port `SUPPORTED_EXTENSIONS` map
   byte-exact).
- **No edits** to `core/extract` analogues; no `dumps_deterministic`/`fingerprint_v3`
  (Class A never hashes). Reuse L0 `Normalization.codePointCompare` for every sort (R-8).

**Slice 4C:** `io.webweavex.ir.DocumentIr` ← `compile_document` (+ `core.evidence` →
`io.webweavex.evidence`, the large pure surface; may span two sessions — port discourse
engines first, evidence engine second).

**Slice 4D:** `io.webweavex.repository.RepositoryExtraction` ← `extract_repository` **after**
the R-2 path-canonicalization harness is approved.

**Slice 4E:** `io.webweavex.connectors.LiveRuntime` ← `run_live_runtime` (aggregates the
already-proven connector four).

**Slice 4F+ (multi-session):** L1b primitives (`io.webweavex.determinism.DeterministicSerializer`,
`io.webweavex.crypto.KaalkaEngine`) → L3a lxml Soup → `extract` family; then L3b html.parser
Soup → `extract_html_file`/`extract_web` DOM core.

---

## Part C — Test strategy & `gen_java_parity_vectors_s4a.py` spec (Phase 6)

> **Specification only — the generator is NOT written this session.**

**How parity is proven (unchanged contract):** the generator imports the canonical Python
`core` from a materialized `origin/python` checkout, runs each target on curated inputs, and
records the **canonical-JSON of the output dict** (for Class A there is no kaalka hash, so the
proof is the serialized output bytes themselves — using `core.serialize`/`json` exactly as the
Python output is structured). The Java `CrossLanguageParityS4ATest` reconstructs the same
inputs, runs the Java port, serializes via the **certified L0 `CanonicalJson`**, and asserts
**byte-equality** against the recorded string. (For any future Class-C slice the entry also
records `dumps_deterministic` + `fingerprint_v3`.)

**Generator shape** (mirrors `tools/gen_java_parity_vectors_s4.py`):
```
python tools/gen_java_parity_vectors_s4a.py java/src/test/resources/parity/golden_vectors_s4a.json
```
imports: `extract_document_runtime`, `extract_paginated_content`, `heal_selector`,
`ingest_input` (+ `extract_archive`, `analyze_document`, `compile_media_ir` if ported).
Each entry: `{ "name", "inputs", "output": <canonical-json string of the Python dict> }`.

**Vector categories (per target):**

*Deterministic / structural —*
- `extract_document_runtime`: empty text; single heading; multi-level heading hierarchy;
  text with citations `[1]`/`(Author, 2024)`; reference list; markdown tables; mixed; with
  `slides=[…]`; with `workbook={…}`; both.
- `extract_paginated_content`: 0 pages; N pages linear; **cycle** (loop_prevented=true);
  `MAX_PAGES=100` boundary (99/100/101); page without `click`.
- `heal_selector`: exact match; missing selector → fallback strategy; multiple candidates
  (ranking + sort stability); empty `dom_nodes`; **empty `html`** (R-7 scope).
- `ingest_input`: one input per branch key (pdf/docx/pptx/xlsx/csv/json/xml/html/markdown/
  text/repository/archive/image/url/unknown); upper-case extension; no extension; bare URL.

*Edge cases —* empty input, whitespace-only, very long text (bounded-slice limits),
duplicate elements (dedup + `sorted(set)` order), null/None optional args.

*Unicode —* astral-plane chars (😀, surrogate pairs), combining marks (NFC vs NFD inputs),
RTL text, CJK, mixed-script — directly exercises R-8 code-point sort & R-9 normalization.

*Normalization —* CRLF vs LF, trailing whitespace, NBSP, zero-width chars (proves L0
`Normalization` is applied identically).

*Repository cases (slice 4D)* — a committed fixture tree under
`java/src/test/resources/parity/repo_fixture/`: nested dirs, `SKIP_DIR_NAMES` dirs present,
each `SUPPORTED_CODE_EXTENSIONS` language, a `SERVICE_FILES`/`INFRA_FILES`/`BUILD_FILES` file,
`@app.route`/`router.get` routes, import edges, a language tie (R-4); generated with a
**relative** root and **separator-normalized** paths (R-2).

*Document cases (slice 4C)* — argumentative text (claims/arguments), tutorial with
prerequisites, coreference chains, concept progression — exercising the discourse + evidence
engines.

**Coverage target:** ≥ 94 % instruction coverage on the new packages (regression gate),
plus every vector category above represented for each shipped API.

---

## Part D — Governance updates (Phase 8.3, applied in slice 4B — NOT now)

Per [`JAVA_BRANCH_POLICY.md`](../JAVA_BRANCH_POLICY.md) §3/§6 and
[`tools/validate_java_manifest.py`](../tools/validate_java_manifest.py):
1. Add to `MAPPING` (validator) — one entry per newly proven API:
   `"extract_document_runtime": ("io.webweavex.documents.DocumentRuntime", "golden_vectors_s4a.json", "extract_document_runtime")`,
   and likewise for `extract_paginated_content` → `io.webweavex.interaction.Pagination`,
   `heal_selector` → `io.webweavex.adaptive.SelectorHealing`,
   `ingest_input` → `io.webweavex.ingestion.Ingestion`.
2. Ship `java/src/test/resources/parity/golden_vectors_s4a.json` (generated).
3. Add `io.webweavex.parity.CrossLanguageParityS4ATest` that **loads `golden_vectors_s4a.json`**
   (satisfies validator check 8) with byte-exact assertions.
4. Regenerate (do not hand-edit) `JAVA_PARITY_MATRIX.md` so the four rows read
   `✅ Implemented (parity-proven)` and the new packages
   (`io.webweavex.documents`, `.interaction`, `.adaptive`, `.ingestion`) appear in the package
   list marked **implemented** (validator check 7).
5. Raise CI `PROVEN_FLOOR` 21 → 25 in the parity-regression workflow.

**Validator checks that will gate the slice:** 1 (in manifest ✓ — all four have
`python:true`), 2 (class exists), 3 (golden section present), 4/9 (matrix row), 5
(`matrix_proven_count == len(MAPPING)` → 25 == 25), 7 (packages documented), 8 (test loads
file), 10 (bidirectional source↔matrix). README check 6 is unaffected.

---

## Part E — Matrix updates (Phase 8.4, slice 4B)

Regenerated by `tools/gen_java_parity_matrix.py` from `PARITY_MANIFEST.json` (never hand-edited):
- `extract_document_runtime`, `extract_paginated_content`, `heal_selector`, `ingest_input` →
  `✅ Implemented (parity-proven)`.
- Summary row `Java implemented (parity-proven)` 21 → 25; `Java planned` 107 → 103.
- Package list: mark `io.webweavex.documents`, `.interaction`, `.adaptive`, `.ingestion`
  **implemented**.
- Note in the matrix that `extract_document_runtime`/`heal_selector` are manifest-Partial but
  Java-proven (cross-reference the governance audit F1).

---

## Part F — Certification requirements (Phase 8.5, slice 4B)

Following the Session-4 precedent, the slice is certified only when **all** hold:
1. `mvn -q -Dtest=CrossLanguageParityS4ATest test` green — byte-exact vs recorded Python.
2. Full `mvn verify` green on the JDK 17 **and** 21 CI matrix.
3. `python tools/validate_java_manifest.py` → `PASS` (25/128, all 10 checks).
4. Instruction coverage ≥ 94 % on new packages; `PROVEN_FLOOR` raised to 25 and the
   regression gate green (proven count never decreased).
5. **No `src/main`** containing `TODO`/`FIXME`/placeholder `UnsupportedOperationException`/
   fabricated return values (policy §5) — explicitly: no injectable network stub smuggled in
   to fake an `extract(url)` vector (R-10).
6. Vectors regenerated **from execution** (not hand-authored); generator committed under
   `tools/`.
7. Emit `java/SESSION_4A_CERTIFICATION.{md,json}` (analysis-phase record) and, when 4B lands,
   `java/SESSION_4B_CERTIFICATION.{md,json}`; update
   [`JAVA_BRANCH_CERTIFICATION.md`](../JAVA_BRANCH_CERTIFICATION.md).

---

## Part G — Out-of-scope guardrails (this session and 4B)

- **Do not** touch `core/extract/pipeline.py` analogues, the Soup engine, or
  `dumps_deterministic`/`fingerprint_v3` in slice 4B — they are gated multi-session work.
- **Do not** stub network/browser/OS to manufacture parity for `extract`(url), `crawl`,
  `extract_web`, `extract_native` — they stay `⬜ Planned`/Deferred.
- **Do not** edit `PARITY_MANIFEST.json` (policy §2).
- `extract_multimodal` (OCR) is the **vision/ocr** layer (matrix session 7), not extraction.
