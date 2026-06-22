# JAVA_SESSION_16_GOVERNANCE_AUDIT

```
$ python tools/validate_java_manifest.py
MANIFEST VALIDATION: PASS — 69/128 APIs proven; mapped/exist/tested/documented;
README Java-native; source<->matrix consistent
$ python tools/gen_java_parity_matrix.py
wrote java/JAVA_PARITY_MATRIX.md (128 APIs, 69 Java-proven)
```

| Metric | Value |
| --- | ---: |
| Proven (validator / matrix / MAPPING) | **69 / 69 / 69** |
| `PROVEN_FLOOR` (CI) | **69** |
| Manifest modified | **no** |

`run_reconstruction_runtime` + `run_reconstruction_for_extraction` in MAPPING + matrix.
README updated (69 / 732 / 96.42 %). Governance gate **PASS**.
