# JAVA_GOVERNANCE_AUDIT

**Machine-verified governance state. All gates PASS.** Generated from repository state at the
current slice (27 proven APIs).

| Gate | Tool / evidence | Result |
| --- | --- | --- |
| Validator | `python tools/validate_java_manifest.py` | **PASS** — `27/128 APIs proven; mapped/exist/tested/documented; README Java-native; source↔matrix consistent` (all 10 checks) |
| Matrix | `tools/gen_java_parity_matrix.py` (regenerated from manifest) | **PASS** — 27 proven, no hand-maintained counts |
| Manifest | `PARITY_MANIFEST.json` present, **unmodified** this mission | **PASS** (policy §2) |
| Parity tests | `mvn verify` | **PASS** — **287 tests, 0 failures, 0 errors** |
| Coverage | JaCoCo | **PASS** — 95.57 % instruction (floor 94 %) |
| Traceability | MAPPING size == matrix proven-count == implemented classes | **PASS** — 27 == 27 == 27 (validator checks 5 & 10) |
| CI floors | `.github/workflows/parity-regression.yml` | `PROVEN_FLOOR=27`, `COVERAGE_FLOOR=94.0` |

## Drift checks (validator checks 1–10)

1. proven API ∈ manifest — ✅ (all 27)
2. mapped class file exists — ✅
3. golden-vector section present — ✅
4/9. documented in matrix — ✅
5. matrix proven-count == MAPPING size (27) — ✅
6. README no foreign install/badge — ✅
7. implemented package documented — ✅ (`connectors`, `documents`, `interaction`, …)
8. parity test loads each golden file — ✅ (`golden_vectors_s7.json` referenced by `CrossLanguageParityS7Test`)
10. bidirectional source↔matrix — ✅

## Conclusion

No governance inconsistency. Implementation may proceed (it did — Session-7 connector cluster).
This audit is re-runnable each slice; any failure halts implementation until fixed (per the
mission's Phase-1 rule).
