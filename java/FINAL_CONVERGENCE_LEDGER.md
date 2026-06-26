# FINAL_CONVERGENCE_LEDGER

**Session-32 four-language convergence ledger (Python==JS==Dart==Java).** Source-derived; Python canonical. Zero unknown.

| Language | Surface |
|---|---|
| Python | 128/128 |
| JavaScript | 128/128 |
| Dart | 110/128 |
| Java | 110/128 |

## Disposition

| Class | Count |
|---|---:|
| FULL PARITY (all 4) | 105 |
| BLOCKED non-portable (Java+Dart) | 13 |
| PARTIAL Java-frontier-blocked only | 5 |
| PARTIAL Dart-pending only | 5 |
| Total | 128 |

## BLOCKED — 13 (non-portable; missing in Java AND Dart; formal proof)

| API | Substrate |
|---|---|
| `crawl` | network |
| `crawl_async` | network |
| `extract` | lxml |
| `extract_async` | lxml |
| `extract_docs` | lxml |
| `extract_native` | platform |
| `extract_recursive` | lxml+network |
| `extract_repo` | lxml |
| `extract_repository` | filesystem |
| `extract_web` | Playwright |
| `run_native_cognition` | platform |
| `stream_extract` | lxml |
| `universal_extract` | OCR/fs |

## PARTIAL — Java frontier-blocked only (5)

Present + vector-certified in Py/JS/Dart; Java port pending/blocked. **S32 frontier reduction: the AST cluster (query_semantics/reason_semantically/compile_repository) is PROVEN PORTABLE — JS ships a hand-written Python-source line/indent scanner (src/ast/pythonAstEngine.ts); analyze/run_canonical_pipeline route through extract (lxml).**

| API | Java status |
|---|---|
| `analyze` | lxml — portable-pending Java port (JS-proven) |
| `compile_repository` | CPython-AST — portable-pending Java port (JS-proven) |
| `query_semantics` | CPython-AST — portable-pending Java port (JS-proven) |
| `reason_semantically` | CPython-AST — portable-pending Java port (JS-proven) |
| `run_canonical_pipeline` | lxml(aggregator) — portable-pending Java port (JS-proven) |

## PARTIAL — Dart-pending only (5)

Present in Py/JS/Java; Dart deferred (portable; needs Dart SDK).

| API | Dart |
|---|---|
| `capture_dom_mutations` | Deferred |
| `capture_websocket_frames` | Deferred |
| `extract_document_runtime` | Partial |
| `extract_infinite_scroll` | Deferred |
| `run_autonomous_extraction` | Partial |

## Convergence statement
**4-way FULL PARITY: 105/128** (S32: +extract_multimodal/+ingest_input via OCR frontier reduction). Remaining portable work: AST cluster (3, JS-proven), universal_extract, the 5 Dart-pending (needs Dart SDK). 13 non-portable require upstream Python canon changes. Zero unknown.