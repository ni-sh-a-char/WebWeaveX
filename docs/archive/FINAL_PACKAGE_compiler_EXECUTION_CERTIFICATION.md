# FINAL PACKAGE COMPILER EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 7 |
| PASS | 4 |
| FAIL | 3 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/compiler/__init__.py` — barrel_export_mismatch:['compile_semantic_pipeline', 'lower_semantic_ir', 'optimize_semantic_pipeline', 'build_semantic_execution_plan', 'optimize_semantic_bytecode']
- `core/compiler/semantic_compiler_pipeline.py` — py=None js=The requested module '../index.js' does not provide an export named 'compileSemanticBytecode'
- `core/compiler/semantic_execution_compiler.py` — py=None js=The requested module '../index.js' does not provide an export named 'compileSemanticBytecode'

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
