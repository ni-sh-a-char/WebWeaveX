# FINAL PACKAGE VM EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 2 |
| PASS | 0 |
| FAIL | 2 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/vm/__init__.py` — barrel_export_mismatch:['SemanticVirtualMachine']
- `core/vm/semantic_vm_engine.py` — py=AttributeError: 'str' object has no attribute 'memory' js=None

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
