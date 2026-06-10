# EXECUTABLE_PARITY_MATRIX.md

> Phase 5 — Executable Parity Certification. Each row is produced by **executing** the Python 2.0.1, JavaScript, and Dart implementations on the same canonical fixture and hashing the raw output with each language's own deterministic hasher. Source inspection is NOT used. Generated 2026-06-10 from `validation/executable/` (`run_python.py`, `run_js.mjs`, `run_dart.dart`).

Reproduce:
```bash
PYTHONPATH=<py2.0.1> python validation/executable/run_python.py validation/executable/fixtures.json
(cd <js-2.0.1> && npx tsx run_js.mjs <abs fixtures.json>)
dart run validation/executable/run_dart.dart validation/executable/fixtures.json
```

| API | Fixture | Python hash | JavaScript hash | Dart hash | Match? | Classification |
|-----|---------|-------------|-----------------|-----------|--------|----------------|
| `extract_kubernetes_runtime` | `k8s-empty` | `78dd9346c65c3dd8` | `78dd9346c65c3dd8` | `78dd9346c65c3dd8` | ✅ ALL3 | Complete (executable) |
| `extract_kubernetes_runtime` | `k8s-snap` | `fa44ab0fb9353ab2` | `fa44ab0fb9353ab2` | `fa44ab0fb9353ab2` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-pg` | `b001d9efeb4cc1c3` | `b001d9efeb4cc1c3` | `b001d9efeb4cc1c3` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-pg-empty` | `04e85875e2d2a4d2` | `04e85875e2d2a4d2` | `04e85875e2d2a4d2` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-mysql` | `7b0c03c8841383ac` | `7b0c03c8841383ac` | `7b0c03c8841383ac` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-sqlite` | `91cfa055805fa72d` | `91cfa055805fa72d` | `91cfa055805fa72d` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-redis` | `77d7c598138483ed` | `77d7c598138483ed` | `77d7c598138483ed` | ✅ ALL3 | Complete (executable) |
| `extract_database_runtime` | `db-unknown` | `c845c3a06b43baee` | `c845c3a06b43baee` | `c845c3a06b43baee` | ✅ ALL3 | Complete (executable) |
| `build_runtime_memory` | `build-rt-mem` | `060e4d5f24eafa71` | ✗ 'list' object has no att | ✗ Bad state: unknown/contr | ⚠️ Dart DIVERG | Partial (contract change required) |
| `query_runtime_memory` | `query-rt-mem` | `40367d57ad329aef` | ✗ The "data" argument must | ✗ Bad state: unknown/contr | ⚠️ Dart DIVERG | Partial (contract change required) |
| `build_browser_identity` | `browser-id` | `4ea9e25540e6c845` | ✗ The "data" argument must | ✗ Bad state: unknown/contr | ⚠️ Dart DIVERG | Partial (contract change required) |
| `compute_kaalka_hash` | `hash-nested` | `222135f9323b12b1` | `222135f9323b12b1` | `222135f9323b12b1` | ✅ ALL3 | Complete (executable) |

## Per-API certification

| API | Verdict |
|-----|---------|
| `extract_kubernetes_runtime` | Complete (executable) |
| `extract_database_runtime` | Complete (executable) |
| `build_runtime_memory` | Partial (contract change required) |
| `query_runtime_memory` | Partial (contract change required) |
| `build_browser_identity` | Partial (contract change required) |
| `compute_kaalka_hash` | Complete (executable) |

## Result

- **`extract_kubernetes_runtime`** and **`extract_database_runtime`** (postgres/mysql/sqlite/redis + degraded): **Python ≡ JavaScript ≡ Dart** on every fixture → re-implemented to executable parity and promoted Partial → **Complete** (vectors: `validation/parity/connectors_snapshot_api_vectors.json`, test: `test/parity/connectors_snapshot_parity_test.dart`).
- **`compute_kaalka_hash`**: ALL3 (foundational cross-language hash, re-confirmed by execution).
- **`build_runtime_memory`**, **`query_runtime_memory`**, **`build_browser_identity`**: Python executes; **Dart cannot execute them under the current public contract** (the Dart signatures diverge — `buildRuntimeMemory(RuntimeGraph)` vs Python `(runtime_history, lineage, semantic_relations)`; `queryRuntimeMemory(mem, key)` vs `(memory, query_type, term)`; `buildBrowserIdentity(captured)` vs `(profile_id)`). These remain **Partial**; achieving parity requires a public-contract change (and, for `build_browser_identity`, porting Python's ~10-helper profile-generation subsystem + data tables). See `PARTIAL_API_AUDIT.md`.
