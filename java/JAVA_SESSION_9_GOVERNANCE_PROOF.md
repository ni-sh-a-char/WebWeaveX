# JAVA_SESSION_9_GOVERNANCE_PROOF

**Phase 4 — governance re-verified live.**

## Validator output

```
$ python tools/validate_java_manifest.py
MANIFEST VALIDATION: PASS — 37/128 APIs proven; mapped/exist/tested/documented;
README Java-native; source<->matrix consistent
```

All 10 checks pass (manifest-present, class-exists, golden-section, matrix-documented,
matrix==mapping count, README, package-documented, parity-test-loads-file, bidirectional
source↔matrix).

## Matrix output

```
$ python tools/gen_java_parity_matrix.py
wrote java/JAVA_PARITY_MATRIX.md (128 APIs, 37 Java-proven)
```

Regenerated identically (no drift). Proven mark count in matrix = **37**.

## Counts

| Metric | Value |
| --- | ---: |
| Proven count (validator) | **37** |
| Proven count (matrix marks) | **37** |
| Validator MAPPING size | **37** |
| `PROVEN_FLOOR` (CI) | **37** |
| Manifest modified this session | **no** |

## Six execution APIs present in governance

| API | validator MAPPING | matrix row |
| --- | :---: | :---: |
| `build_runtime_sandbox` | ✓ | ✅ proven |
| `execute_runtime_action` | ✓ | ✅ proven |
| `replay_runtime_execution` | ✓ | ✅ proven |
| `simulate_runtime_execution` | ✓ | ✅ proven |
| `run_execution_runtime` | ✓ | ✅ proven |
| `run_execution_for_extraction` | ✓ | ✅ proven |

All six present and consistent across validator MAPPING and matrix. Governance gate **PASS**.
