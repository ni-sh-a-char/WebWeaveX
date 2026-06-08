# FINAL PACKAGE REASONING EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 9 |
| PASS | 2 |
| FAIL | 7 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/reasoning/__init__.py` — barrel_export_mismatch:['reason_semantically', 'reason_topology_semantic', 'reason_runtime_semantic', 'reason_discourse_semantic', 'traverse_with_constraints']
- `core/reasoning/discourse_reasoning_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/reasoning/runtime_reasoning_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/reasoning/semantic_proof_runtime.py` — output_or_state_mismatch
- `core/reasoning/semantic_reconciliation_query_engine.py` — output_or_state_mismatch
- `core/reasoning/semantic_traversal_runtime.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\query\semanticTraversalEngine.ts:42:7: ERROR: Expected ")" but found ":"
- `core/reasoning/topology_reasoning_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\graph\semanticCycleAnalysisEngine.ts:22:7: ERROR: Expected ")" but found ":"

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
