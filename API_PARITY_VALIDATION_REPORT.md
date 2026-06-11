# API_PARITY_VALIDATION_REPORT.md

> **Generated from `PARITY_MANIFEST.json`** by `tools/generate_reports.py`. No hand-maintained counts. Python 2.0.1 is canonical; JavaScript is the reference.

## Counts (manifest)

| Status | Count |
|--------|------:|
| ✅ Complete | **105** |
| 🟡 Partial | **18** |
| ⚪ Deferred | **5** |
| ❌ Missing | **0** |
| **Total Python APIs** | **128** |

## Proof-type breakdown (functional Complete APIs)

| Proof type | Count |
|------------|------:|
| VECTOR | 62 |
| CORE_VECTOR | 4 |
| ROUNDTRIP | 26 |

## Executable-proven APIs (14)

Proven **Python ≡ JavaScript ≡ Dart** by execution on shared fixtures (`validation/executable/`, `EXECUTABLE_PARITY_MATRIX.md`):

- `build_browser_identity`
- `build_runtime_memory`
- `compute_global_runtime_fingerprint`
- `compute_kaalka_hash`
- `execute_runtime_objective`
- `extract_container_runtime`
- `extract_database_runtime`
- `extract_ide_runtime`
- `extract_kubernetes_runtime`
- `get_runtime_kernel`
- `query_runtime_graph`
- `query_runtime_memory`
- `reconstruct_runtime`
- `validate_replay_equivalence`

## Verdict

- **0 Missing.** 105 Complete, 18 Partial, 5 Deferred of 128 canonical APIs.
- Every Complete API has executable or vector/roundtrip proof (`COMPLETE_API_PROOF_MATRIX.md`). Every Partial/Deferred is classified with a reason (`PARTIAL_API_AUDIT.md`, `DEFERRED_API_AUDIT.md`).
