# LEGACY PURGE REPORT

**WebWeaveX v2.0.0 — absolute hardening pass**

## Deleted paths

| Path | Reason |
|------|--------|
| `core/legacy/` | Deprecated Phase-7 engines; zero active pipeline imports |
| `core/security/v2/` | Superseded by `core/security/`; only legacy test referenced |
| `core/security/v3/` | Superseded by `core/security/`; only legacy test referenced |
| `core/adaptive_engine.py` | Shim re-export to deleted legacy |
| `core/artifact_engine.py` | Shim re-export to deleted legacy |
| `core/compiler_engine.py` | Shim re-export to deleted legacy |
| `core/execution_engine.py` | Shim re-export to deleted legacy |
| `core/reasoning_engine.py` | Shim re-export to deleted legacy |
| `core/semantic_engine.py` | Shim re-export to deleted legacy |
| `core/system_inference.py` | Shim re-export to deleted legacy |
| `tests/final_validation_v15.py` | Required deleted `security.v2` |
| `tests/final_validation_v16.py` | Required deleted `security.v3` |

## Migrated paths

| Before | After |
|--------|-------|
| Multiple parallel pipelines | `core/kernel/runtime_pipeline.py` |
| Volatile browser IR | `core/browser/dom_stabilization_engine.py` + `spa_runtime_stabilizer.py` |
| Legacy crypto experiments | `core/crypto/kaalka_runtime_engine` (only) |

## Preserved compatibility

- Public API unchanged: `extract_web`, `extract_repository`, `run_canonical_pipeline`, `RuntimeKernel`
- `import webweavex` remains the supported entry point
