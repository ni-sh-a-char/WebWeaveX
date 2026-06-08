# FINAL PACKAGE SSA EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 3 |
| PASS | 0 |
| FAIL | 3 |
| UNTESTED | 0 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/ssa/__init__.py` — barrel_export_mismatch:['build_ssa_form', 'build_multilang_ssa']
- `core/ssa/multilang_ssa_engine.py` — output_or_state_mismatch
- `core/ssa/ssa_builder_engine.py` — py=None js=ast is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
