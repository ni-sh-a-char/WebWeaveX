# SESSION 4B CERTIFICATION

**Slice:** pure document + pagination extraction — the two APIs that survive the Session-4B
dependency proof. Branch `java`. Python canon `origin/python` @ `9625f4a` (2.1.0).

## Pre-implementation gate

[`JAVA_SESSION_4B_DEPENDENCY_PROOF.md`](JAVA_SESSION_4B_DEPENDENCY_PROOF.md) — AST transitive
import trace (`tools/trace_imports_s4b.py`, result `tools/trace_result_s4b.json`):

| Candidate | Verdict | Reason |
| --- | --- | --- |
| `extract_document_runtime` | ✅ SURVIVES | 10-module closure, stdlib only (`re`, `typing`) |
| `extract_paginated_content` | ✅ SURVIVES | 1 module, self-contained |
| `heal_selector` | ❌ REMOVED | `bs4` via `core.adaptive.semantic_anchor_engine` |
| `ingest_input` | ❌ REMOVED | `pytesseract`+`PIL` (OCR) via `core.ocr.ocr_engine` |

No BeautifulSoup / lxml / browser / OCR / PDF / DOCX / network / LLM dependency in either
implemented API.

## Implemented APIs (2)

| Manifest API | Java class | Python canon |
| --- | --- | --- |
| `extract_document_runtime` | `io.webweavex.documents.DocumentRuntime#extractDocumentRuntime` | `core.documents.universal_document_extraction_engine` (+ structure/hierarchy/citation/reference/table/knowledge-graph/presentation/spreadsheet engines + `core.ir.document_runtime_ir`) |
| `extract_paginated_content` | `io.webweavex.interaction.Pagination#extractPaginatedContent` | `core.interaction.pagination_engine` |

Supporting (internal, no stubs): `io.webweavex.determinism.PyText` (CPython
`splitlines`/`strip`/`lstrip`), `io.webweavex.interaction.PageView` (duck-typed page contract).

## Parity proof

- Generator: `tools/gen_java_parity_vectors_s4b.py` (imports canonical `core`).
- Vectors: `java/src/test/resources/parity/golden_vectors_s4b.json` — **26** vectors
  (15 `extract_document_runtime` + 11 `extract_paginated_content`), covering Unicode (CJK,
  astral emoji, combining marks, Arabic-Indic citation digits), normalization (CRLF, trailing
  whitespace, NBSP, zero-width), empty/whitespace inputs, malformed inputs (bare `#`, empty
  brackets, ragged tables, pipe-only lines, heading-after-heading), edge cases (MAX_PAGES=100
  boundary), and replay/traversal cases (linear, cycle/loop-prevention, click-raises,
  url-fallback, Unicode URLs).
- Test: `io.webweavex.parity.CrossLanguageParityS4BTest` — every vector asserts
  `stable_serialize` **and** `compute_kaalka_hash` byte-equal to recorded Python.
- Result: **26/26 byte-exact** (Java ≡ Python ⇒ Java ≡ JS ≡ Dart transitively).

## Counts

| Metric | Before (S4) | After (S4B) |
| --- | --- | --- |
| Parity-proven manifest APIs | 21 | **23** |
| Remaining (of 128) | 107 | **105** |
| Total tests | 208 | **249** (+26 parity, +15 unit) |
| Instruction coverage | 94.91% | **95.37%** |
| New-code coverage (documents+interaction+PyText) | — | **99.06%** |

## Governance

- `tools/validate_java_manifest.py` — `MAPPING` +2 entries → **PASS 23/128** (all 10 checks:
  manifest-present, class-exists, golden-section, matrix-documented, package-documented,
  parity-test-loads-file, bidirectional source↔matrix, README Java-native).
- `java/JAVA_PARITY_MATRIX.md` — regenerated from `PARITY_MANIFEST.json`; `documents` and
  `interaction` packages marked implemented; proven count 23.
- `.github/workflows/parity-regression.yml` — `PROVEN_FLOOR` 21 → **23**; coverage floor 94.0%
  (now 95.37%).
- `PARITY_MANIFEST.json` — **not modified** (policy §2).

## Gate compliance

No stubs / TODO / placeholder in `src/main`; no network/browser/OCR shim introduced. No
manifest edit. Coverage increased. `mvn verify` BUILD SUCCESS (249/0/0). Validator PASS.
