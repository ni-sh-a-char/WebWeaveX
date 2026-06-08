# FINAL PACKAGE EVOLUTION EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 21 |
| PASS | 15 |
| FAIL | 6 |
| UNTESTED | 0 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/evolution/__init__.py` — barrel_export_mismatch:['evolve_semantic_runtime', 'suggest_semantic_refactors', 'orchestrate_semantic_evolution', 'optimize_semantic_architecture', 'analyze_semantic_dependencies']
- `core/evolution/semantic_evolution_orchestrator.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/evolution/semantic_graph_reconciliation_engine.py` — py=None js=n is not defined
- `core/evolution/semantic_repository_diff_engine.py` — py=None js=(right_keys - left_keys) is not iterable
- `core/evolution/semantic_runtime_drift_engine.py` — output_or_state_mismatch
- `core/evolution/semantic_topology_evolution_engine.py` — py=None js=idx is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
