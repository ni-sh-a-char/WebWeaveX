# FINAL PACKAGE AST EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 6 |
| PASS | 3 |
| FAIL | 3 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/ast/__init__.py` — barrel_export_mismatch:['parse_python_ast', 'resolve_symbols', 'build_control_flow_graph', 'reconstruct_execution_paths', 'compile_semantic_ast_ir']
- `core/ast/python_ast_engine.py` — python_import:No module named 'core.astthon_ast_engine'
- `core/ast/semantic_ast_ir_engine.py` — py=None js=ast is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
