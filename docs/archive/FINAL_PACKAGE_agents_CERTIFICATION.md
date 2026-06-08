# FINAL PACKAGE AGENTS EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 13 |
| PASS | 9 |
| FAIL | 4 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/agents/__init__.py` — barrel_export_mismatch:['SemanticAgent', 'SemanticAgentRuntime', 'build_semantic_task_graph', 'route_semantic_capability']
- `core/agents/semantic_agent_engine.py` — py=AttributeError: 'str' object has no attribute 'agent_id' js=Class constructor SemanticAgent cannot be invoked without 'new'
- `core/agents/semantic_agent_runtime.py` — py=AttributeError: 'str' object has no attribute '_agents' js=Class constructor SemanticAgentRuntime cannot be invoked without 'new'
- `core/agents/traversal_query_engine.py` — py=None js=e is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
