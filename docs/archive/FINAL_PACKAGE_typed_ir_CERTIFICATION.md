# FINAL PACKAGE TYPED_IR EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 5 |
| PASS | 1 |
| FAIL | 3 |
| UNTESTED | 1 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/typed_ir/__init__.py` — barrel_export_mismatch:['SemanticNode', 'SemanticEdge', 'ExecutionState', 'RuntimeTransition', 'compile_typed_repository_ir']
- `core/typed_ir/typed_repository_ir.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/typed_ir/typed_runtime_ir.py` — py=None js=s is not defined

## UNTESTED

- `core/typed_ir/schema_types.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
