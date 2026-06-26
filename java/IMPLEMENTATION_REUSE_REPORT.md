# IMPLEMENTATION_REUSE_REPORT

**Session-33 cross-language reuse map — what each language already solved, and the reuse roadmap for
closing the remaining Java (and Dart) gaps. Mandatory per the directive: never reinvent an algorithm
already implemented elsewhere.** Source-derived.

## What each language has solved (and how)

| Cluster | Python (canonical) | JavaScript | Dart | Java |
|---|---|---|---|---|
| **OCR** (`extract_multimodal`/`ingest_input`) | real `pytesseract`, but vectors generated OCR-absent | hardcodes `pytesseract = null` → `ocr_dependencies_missing` (`src/ocr/ocrEngine.ts`) | OCR-absent contract | **DONE (S32)** — `MultimodalRuntime`, ported from the no-OCR contract |
| **AST** (`query_semantics`/`reason_semantically`/`compile_repository`) | real `import ast` (`core/ast/python_ast_engine.py`) | hand-written 204-line line/indent scanner (`src/ast/pythonAstEngine.ts`) reproducing `ast.walk` summary | scanner port | **pending** — port the JS scanner + the AST sub-engines (symbol/cfg/execution-path, 83 L) + the `repository-semantic-IR` subsystem (~3600 L epistemic engine) for the repository/runtime branch |
| **lxml extraction** (`extract` family, 8 APIs) | `BeautifulSoup(text,"lxml")` | reproduced extraction on **1200 real URLs, 0% drift** (lxml-equivalent parser) | partial | **pending** — port the JS HTML parser |
| **network** (`crawl`/`crawl_async`) | `requests`/`httpx` + regex link discovery | reproduced via fetch + same regex | partial | **pending** — regex engine is portable; needs a fetch-fixture contract |
| **Playwright** (`extract_web`) | live Chromium | reproduced via the unavailable/stub contract | partial | **pending** — stub-page/unavailable contract |
| **platform/fs** (`extract_native`/`run_native_cognition`/`extract_repository`) | `sys.platform`/`os.walk` | reproduced via normalized/degraded fields | partial | **pending** — platform-string + missing-file contracts |

## Frontier correction (Session 33 — measured, supersedes prior estimate)

`compile_repository_ir`'s **observable output is epistemic-free** (zero `uncertainty`/`entropy`/
`epistemic`/`observed`/`inferred` fields; serialized ~3.2 KB). The ~2776-line `core.evidence` engine is
imported but its result is fully **discarded** (the S22 `query_documents` pattern). The real
runtime-observable closure of the AST cluster is **~1389 lines** (repository code-analysis + AST), NOT
the ~3600-line epistemic engine. This makes the AST cluster materially more tractable than previously
recorded.

## Reuse roadmap for Java (priority order, all PORTABLE — none impossible)

1. **AST scanner** — ✅ **DONE (S33)**: `io.webweavex.ast.PythonAstEngine` + `SemanticAstIr` ported from
   the JS scanner (`src/ast/pythonAstEngine.ts`) + the 3 tiny sub-engines, **certified byte-exact vs
   real CPython `ast.walk`** (`AstEngineUnitTest`, 14 vectors). Corrected two CPython-semantics
   divergences the JS scanner had latent (`*args` exclusion; tuple-target `b,c=…` → `[]`). Reusable
   foundation for the AST cluster.
2. **repository code-analysis layer** (~1100 L, ~30 small modules — `build_repository_execution_ir`,
   language/dependency/service/deployment/api/infra/execution-flow detection; **epistemic-free**) →
   port on top of #1 to certify `query_semantics`/`reason_semantically`/`compile_repository`. Bounded,
   multi-session; no epistemic engine needed (frontier correction above). The document/graph/knowledge
   branches already reuse certified Java engines (`DocumentSemanticIr` S22, `GraphQuery`/`OntologyQuery`
   S3).
3. **HTML parser** (lxml-equivalent) → port the JS parser to unblock the 8-API lxml cluster. Large.
4. **universal_extract** → port the file extractors (pdf/docx/archive/html_file deterministic missing-file paths) + reuse #2 for the repository branch.
5. **network/Playwright/platform/fs** → port the regex/stub/missing-file/platform-string contracts.

## Reuse roadmap for Dart
Dart already has 110/128. Its 5 unique gaps (`capture_dom_mutations`, `capture_websocket_frames`,
`extract_document_runtime`, `extract_infinite_scroll`, `run_autonomous_extraction`) are **already
solved in Java** (S28/S30/S4B) and Python/JS — port those Java/JS implementations to Dart. **Requires
the Dart SDK, which is absent in this environment** (cannot compile/byte-exact-verify Dart here).

## Principle applied
Every remaining port reuses an existing-language solution (JS for AST/lxml/OCR; Java for the 5
Dart-pending). No algorithm is reinvented; none is impossible.
