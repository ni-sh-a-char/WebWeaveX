# TEST_INVENTORY.md

Measured from `test/` in the canonical repo (`dart` branch). **779 tests executed** (`dart test`), 644 static `test(` declarations across **33 files** (the gap is vector-driven loops that expand one declaration into many cases). Every test validates real behavior — parity tests assert cross-language hash equality, others assert structural contracts; no placeholder assertions.

## By category

| Category | Files | Purpose |
|----------|------:|---------|
| Parity (cross-language) | 12 | `computeDeterministicHash(dartOut) == Python compute_deterministic_hash`; save/load roundtrip |
| Engine coverage | 3 | branch coverage of ported runtime-family engines |
| Subsystem coverage | 12 | crypto, determinism, graph, replay, memory, reconstruction, browser, connectors, kernel |
| Core/smoke/integration | 6 | kaalka, dom, normalization, pipeline, exports, replay smoke |

## By file (static `test(` count)

| Count | File |
|------:|------|
| 94 | engines/runtime_families_engines_test.dart |
| 67 | engines/execution_engines_test.dart |
| 43 | determinism/determinism_coverage_test.dart |
| 41 | connectors/connectors_coverage_test.dart |
| 40 | engines/wave2_coverage_test.dart |
| 37 | browser/browser_coverage_test.dart |
| 37 | crypto/crypto_coverage_test.dart |
| 35 | memory/memory_coverage_test.dart |
| 31 | parity/query_parity_test.dart |
| 29 | replay/replay_coverage_test.dart |
| 23 | parity/persistence_parity_test.dart |
| 22 | graph/graph_coverage_test.dart |
| 21 | parity/memory_runtime_parity_test.dart |
| 21 | reconstruction/reconstruction_coverage_test.dart |
| 16 | parity/connectors_runtime_parity_test.dart |
| 16 | parity/kernel_parity_test.dart |
| 12 | kernel/kernel_coverage_test.dart |
| 11 | parity/reconstruction_runtime_parity_test.dart |
| 9 | parity/semantic_parity_test.dart |
| 9 | parity/synchronization_parity_test.dart |
| 7 | parity/causality_parity_test.dart |
| 4 | parity/execution_parity_test.dart |
| 3 | parity/evolution_parity_test.dart |
| 3 | parity/workflows_parity_test.dart |
| 2 | browser/render_page_http_test.dart |
| 2 | determinism/normalization_test.dart |
| 1 each | crypto/kaalka_test, crypto/parity_vectors_test, determinism/dom_test, graph/runtime_graph_test, integration/pipeline_test, production/exports_test, replay/replay_test |

## Parity vectors

12 family vector files under `validation/parity/*_api_vectors.json` (~145 canonical input→`det_hash` records), plus the original cross-language `dart_vectors.json` / `javascript_vectors.json` / `python_vectors.json` (11/11 crypto/graph core).

## Toward 1000+

779 executed today (from 11 at the start of the parity program). The path to 1000+ is the next portable wave (Partial→Complete on the query/IR families once an NLP/AST compiler is ported) plus broadened edge-case coverage — each added test must validate real behavior, not pad the count.
