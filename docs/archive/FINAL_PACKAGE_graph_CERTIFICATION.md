# FINAL PACKAGE GRAPH EXECUTION CERTIFICATION

**Measured:** 2026-06-04T13:01:42.247784+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 37 |
| PASS | 17 |
| FAIL | 20 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/graph/__init__.py` — barrel_export_mismatch:['MAX_EDGES', 'MAX_NODES', 'bound_graph_memory', 'build_semantic_graph_from_ids', 'normalize_graph_nodes']
- `core/graph/dependency_proof_engine.py` — output_or_state_mismatch
- `core/graph/graph_compression_engine.py` — py=None js=merged_edges.extend is not a function
- `core/graph/graph_consistency_prover.py` — py=None js=enumerate is not defined
- `core/graph/graph_entropy_engine.py` — output_or_state_mismatch
- `core/graph/graph_partition_engine.py` — py=None js=range is not defined
- `core/graph/graph_reconciliation_engine.py` — py=None js=graphs is not defined
- `core/graph/reasoning/__init__.py` — barrel_export_mismatch:['semantic_paths', 'graph_similarity', 'graph_diff', 'graph_search', 'graph_memory_bound']
- `core/graph/reasoning/graph_diff_engine.py` — py=None js=(be - ae) is not iterable
- `core/graph/reasoning/graph_memory_engine.py` — py=None js=merged_edges.extend is not a function
- `core/graph/reasoning/graph_partition_engine.py` — py=None js=range is not defined
- `core/graph/reasoning/semantic_path_engine.py` — py=None js=undefined is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/graph/semantic_causality_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/graph/semantic_cycle_analysis_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\graph\semanticCycleAnalysisEngine.ts:22:7: ERROR: Expected ")" but found ":"
- `core/graph/semantic_dependency_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/graph/semantic_edge_validation_engine.py` — py=None js=edge.includes is not a function
- `core/graph/semantic_graph_validator.py` — py=None js=enumerate is not defined
- `core/graph/semantic_partition_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\graph\semanticPartitionEngine.ts:14:8: ERROR: Expected ")" but found ":"
- `core/graph/semantic_topology_validator.py` — py=None js=Cannot convert undefined or null to object
- `core/graph/service_graph_engine.py` — py=None js=range is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
