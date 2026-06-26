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

## Reuse roadmap for Java (priority order, all PORTABLE — none impossible)

1. **AST scanner** → port `src/ast/pythonAstEngine.ts` (204 L) verbatim to `io.webweavex.ast.PythonAstEngine` + the 3 tiny sub-engines (`symbol_resolution`/`control_flow`/`execution_path`, 83 L). This grounds `reason_semantically(discourse|topology)` and `query_semantics(document|graph|knowledge|unknown)` immediately (those branches already reuse certified Java engines: `DocumentSemanticIr` S22, `GraphQuery`/`OntologyQuery` S3).
2. **repository-semantic-IR subsystem** (~3600 L, shared by the repository/runtime branch of all 3 AST APIs and by `compile_repository`) — port `build_repository_execution_ir` + the `core.evidence` epistemic engine. Largest single item; multi-session. Dart deferred this too.
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
