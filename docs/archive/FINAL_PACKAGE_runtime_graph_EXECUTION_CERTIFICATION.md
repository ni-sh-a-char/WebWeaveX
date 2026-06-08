# FINAL PACKAGE RUNTIME_GRAPH EXECUTION CERTIFICATION

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

- `core/runtime_graph/__init__.py` — barrel_export_mismatch:['build_runtime_graph', 'resolve_canonical_entity', 'link_runtime_entities', 'query_runtime_graph', 'diff_runtime_graphs']
- `core/runtime_graph/entity_resolution_engine.py` — py=None js=canonical.encode is not a function
- `core/runtime_graph/runtime_graph_diff_engine.py` — py=None js=x is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
