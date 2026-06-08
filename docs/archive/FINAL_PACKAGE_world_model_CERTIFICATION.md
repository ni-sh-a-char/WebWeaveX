# FINAL PACKAGE WORLD_MODEL EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 16 |
| PASS | 9 |
| FAIL | 6 |
| UNTESTED | 1 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/world_model/__init__.py` — barrel_export_mismatch:['build_repository_world_model', 'build_semantic_architecture_graph', 'analyze_semantic_impact', 'build_cross_file_dependencies', 'build_semantic_ownership_graph']
- `core/world_model/cross_file_dependency_engine.py` — py=None js=ir is not defined
- `core/world_model/distributed_repository_traversal_engine.py` — py=None js=deque is not defined
- `core/world_model/repository_world_model_engine.py` — py=None js=null is not iterable
- `core/world_model/semantic_execution_forecast_engine.py` — py=None js=null is not iterable
- `core/world_model/semantic_refactor_engine.py` — py=None js=null is not iterable

## UNTESTED

- `core/world_model/repository_semantic_memory_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
