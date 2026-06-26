# IMPLEMENTATION_REUSE_MATRIX

**Session-33 per-subsystem reuse matrix — which language already solved each subsystem, so Java/Dart
ports reuse rather than reinvent (Rule 3). Source-derived.**

| Subsystem | Python | JavaScript | Dart | Java | Reuse source for remaining ports |
|---|---|---|---|---|---|
| determinism / crypto / hashing | ✅ | ✅ | ✅ | ✅ | — (4-way done) |
| runtime graph / IR / kernel | ✅ | ✅ | ✅ | ✅ | — |
| query / memory / reconstruction | ✅ | ✅ | ✅ | ✅ | — |
| execution / sync / workflow / evolution / causality | ✅ | ✅ | ✅ | ✅ | — |
| streaming / interaction (stub-page) | ✅ | ✅ | ✅(partial) | ✅ | Java for Dart's 5 gaps |
| identity / application / semantic | ✅ | ✅ | ✅ | ✅ | — |
| connectors / persistence | ✅ | ✅ | ✅ | ✅ | — |
| distributed scheduler | ✅ | ✅ | ✅(partial) | ✅ | Java |
| **OCR / multimodal** | ✅ | ✅ (pytesseract=null) | ✅ | ✅ **(S32)** | JS no-OCR contract |
| **AST summary scanner** | ✅ (real `ast`) | ✅ (line/indent scanner) | ✅ | ✅ **(S33)** | JS scanner (Java now more CPython-faithful) |
| **AST parser pipeline** (`parse_source`, symbols/calls/deps, text+python paths) | ✅ | ✅ | ✅ | ⏳ pending | **JS** (`src/parsers/*`) + Python regex engines |
| **repository IR** (`compile_repository_ir`, epistemic-free) | ✅ | ✅ | ✅(partial) | ⏳ pending | **JS** (`src/repository/*`, `src/ir/repositoryIr`) |
| **lxml HTML extraction** | ✅ (`bs4`) | ✅ (1200-URL 0-drift parser) | ✅(partial) | ⏳ pending | **JS HTML parser** |
| network crawl | ✅ (`requests`) | ✅ (fetch + regex) | ✅(partial) | ⏳ pending | JS regex + fetch-fixture contract |
| Playwright extract_web | ✅ | ✅ (stub/unavailable) | ✅(partial) | ⏳ pending | JS stub contract |
| platform / native / fs | ✅ (`sys.platform`/`os.walk`) | ✅ (normalized) | ✅(partial) | ⏳ pending | JS normalized contract |
| `universal_extract` | ✅ | ✅ | ✅(partial) | ⏳ pending | JS file extractors + repository IR |

## Rule-3 reuse plan for the remaining Java ports
1. **AST parser pipeline + repository IR** → port JS `src/parsers/*` + `src/repository/*` +
   `src/ir/repositoryIr.ts` (epistemic-free per `FRONTIER_ANALYSIS.md`). Certifies the AST cluster.
2. **lxml** → port the JS HTML parser (`src/browser/*` / `src/parsers/htmlParser`).
3. **network / Playwright / platform / fs** → port the JS degraded/stub/normalized contracts.

## Rule-3 reuse plan for Dart (needs Dart SDK — absent in this env)
Dart's 5 unique gaps (`capture_dom_mutations`, `capture_websocket_frames`, `extract_document_runtime`,
`extract_infinite_scroll`, `run_autonomous_extraction`) are already solved in Java (S28/S30/S4B) and
JS — port those.

**No subsystem requires a net-new algorithm; every remaining port reuses an existing-language
implementation.**
