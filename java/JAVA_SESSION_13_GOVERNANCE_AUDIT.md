# JAVA_SESSION_13_GOVERNANCE_AUDIT

**Phase 8 — governance verified live.**

## Validator
```
$ python tools/validate_java_manifest.py
MANIFEST VALIDATION: PASS — 61/128 APIs proven; mapped/exist/tested/documented;
README Java-native; source<->matrix consistent
```
All 10 checks pass.

## Matrix
```
$ python tools/gen_java_parity_matrix.py
wrote java/JAVA_PARITY_MATRIX.md (128 APIs, 61 Java-proven)
```
Regenerates identically (no drift). Proven mark count = **61**.

## Counts

| Metric | Value |
| --- | ---: |
| Proven (validator) | **61** |
| Proven (matrix marks) | **61** |
| Validator MAPPING size | **61** |
| `PROVEN_FLOOR` (CI) | **61** |
| Manifest modified | **no** |

## Five causality APIs in governance

| API | MAPPING | matrix |
| --- | :---: | :---: |
| `run_causality_runtime` | ✓ | ✅ |
| `replay_causal_runtime` | ✓ | ✅ |
| `run_causality_for_extraction` | ✓ | ✅ |
| `save_causal_memory` | ✓ | ✅ |
| `load_causal_memory` | ✓ | ✅ |

README metrics updated (61 / 646 / 96.38 %; floor 61); `causality` package marked implemented.
Governance gate **PASS**.
