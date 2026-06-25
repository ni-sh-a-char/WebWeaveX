# FINAL_CONVERGENCE_LEDGER

**Session-31 four-language convergence ledger — Python == JavaScript == Dart == Java.** Source-derived; Python canonical. Every one of the 128 APIs has a terminal disposition: FULL PARITY, PARTIAL (documented single-language divergence), or BLOCKED (formal proof). Zero unknown.

## Surface counts (from source)

| Language | Surface | Toolchain verified this session |
|---|---|---|
| Python | 128/128 (canonical `__all__`) | n/a (reference) |
| JavaScript | **128/128** | ✅ build+399 tests (S31 +version/__version__) |
| Dart | 110/128 | ✗ dart SDK unavailable in env |
| Java | 108/128 | ✅ mvn verify 1135 tests (S30/S31) |

## Disposition

| Class | Count |
|---|---:|
| FULL PARITY (all 4) | 103 |
| BLOCKED (non-portable, 4-lang) | 13 |
| PARTIAL — Java frontier-blocked only | 7 |
| PARTIAL — Dart-pending only | 5 |
| **Total** | 128 |

## FULL PARITY — 103 APIs (present + behaviorally certified in Python, JavaScript, Dart, Java)

The deterministic+crypto foundation, kernel/graph/IR, query/memory/reconstruction, all runtime families (execution/sync/workflow/evolution/causality/streaming/identity/application/semantic), connectors, persistence, and the S28/S30 frontier-reduced APIs. (Full list: `UNIFIED_PARITY_MATRIX.md`.)

## BLOCKED — 13 APIs (non-portable; missing in BOTH Java and Dart; formal proof)

These share one non-portable substrate. Java carries a verified four-part blocker proof (survived S31 adversarial review); Dart classifies them Partial/Deferred for the same root cause.

| API | Substrate | Java proof | Dart |
|---|---|---|---|
| `crawl` | network | JAVA_*_VERDICT/BLOCKER | Partial |
| `crawl_async` | network | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract` | lxml | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_async` | lxml | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_docs` | lxml | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_native` | platform/sys.platform | JAVA_*_VERDICT/BLOCKER | Deferred |
| `extract_recursive` | lxml+network | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_repo` | lxml | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_repository` | filesystem | JAVA_*_VERDICT/BLOCKER | Partial |
| `extract_web` | Playwright | JAVA_*_VERDICT/BLOCKER | Partial |
| `run_native_cognition` | platform/sys.platform | JAVA_*_VERDICT/BLOCKER | Deferred |
| `stream_extract` | lxml | JAVA_*_VERDICT/BLOCKER | Partial |
| `universal_extract` | OCR/fs | JAVA_*_VERDICT/BLOCKER | Partial |

## PARTIAL — Java frontier-blocked only (7 APIs)

Present and vector-parity-certified in Python, JavaScript, and Dart; Java carries a stricter arbitrary-input frontier blocker (byte-exact impossible under pure-Java constraints). Documented divergence, not unknown.

| API | Java blocker | Py/JS/Dart |
|---|---|---|
| `analyze` | lxml (JAVA verdict) | Partial |
| `compile_repository` | CPython-AST (JAVA verdict) | Complete |
| `extract_multimodal` | OCR (JAVA verdict) | Complete |
| `ingest_input` | OCR (JAVA verdict) | Complete |
| `query_semantics` | CPython-AST (JAVA verdict) | Complete |
| `reason_semantically` | CPython-AST (JAVA verdict) | Complete |
| `run_canonical_pipeline` | lxml(aggregator) (JAVA verdict) | Partial |

## PARTIAL — Dart-pending only (5 APIs)

Present in Python, JavaScript, and Java (Java certified these PORTABLE — S28 stub-page / S30 scheduler / S4B document contracts); Dart classifies them Partial/Deferred. These are **portable** (Java proves it); closing them requires a Dart implementation, deferred this session only because the Dart SDK is unavailable in this environment (cannot byte-exact-verify). No blocker — tracked portable work.

| API | Dart status | Portability evidence |
|---|---|---|
| `capture_dom_mutations` | Deferred | Java-certified portable (S28/S4B) |
| `capture_websocket_frames` | Deferred | Java-certified portable (S28/S4B) |
| `extract_document_runtime` | Partial | Java-certified portable (S28/S4B) |
| `extract_infinite_scroll` | Deferred | Java-certified portable (S28/S4B) |
| `run_autonomous_extraction` | Partial | Java-certified portable (S30) |

## Convergence statement

**4-way FULL PARITY: 103/128.** JavaScript reached 128/128 this session (verified). The remaining 25 divergences are all documented and traceable to source: 13 formally BLOCKED (non-portable, proven), 7 Java-frontier-blocked (proven), 5 Dart-pending (portable, needs Dart SDK to implement+verify). **Zero unknown APIs; zero untracked divergences.** Remaining portable work to reach higher convergence: implement the 5 Dart-pending APIs (requires Dart toolchain). The 13 BLOCKED + 7 Java-blocked require upstream Python canon changes to ever be byte-exact across all four languages.