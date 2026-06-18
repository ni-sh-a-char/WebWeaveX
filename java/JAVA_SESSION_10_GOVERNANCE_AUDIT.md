# JAVA_SESSION_10_GOVERNANCE_AUDIT

**Phase 8 — governance verified live.**

## Validator
```
$ python tools/validate_java_manifest.py
MANIFEST VALIDATION: PASS — 43/128 APIs proven; mapped/exist/tested/documented;
README Java-native; source<->matrix consistent
```
All 10 checks pass.

## Matrix
```
$ python tools/gen_java_parity_matrix.py
wrote java/JAVA_PARITY_MATRIX.md (128 APIs, 43 Java-proven)
```
Regenerates identically (no drift). Proven mark count = **43**.

## Counts

| Metric | Value |
| --- | ---: |
| Proven (validator) | **43** |
| Proven (matrix marks) | **43** |
| Validator MAPPING size | **43** |
| `PROVEN_FLOOR` (CI) | **43** |
| Manifest modified | **no** |

## Six synchronization APIs in governance

| API | MAPPING | matrix |
| --- | :---: | :---: |
| `build_runtime_delta` | ✓ | ✅ |
| `replay_synchronized_runtime` | ✓ | ✅ |
| `run_synchronized_runtime` | ✓ | ✅ |
| `run_sync_for_extraction` | ✓ | ✅ |
| `save_sync_memory` | ✓ | ✅ |
| `load_sync_memory` | ✓ | ✅ |

README metrics updated (43 / 503 / 96.13 %; floor 43). Governance gate **PASS**.
