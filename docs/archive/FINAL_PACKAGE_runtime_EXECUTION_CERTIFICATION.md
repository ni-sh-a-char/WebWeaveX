# FINAL PACKAGE RUNTIME EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 56 |
| PASS | 18 |
| FAIL | 28 |
| UNTESTED | 10 |
| Hash mismatches | 8 |
| State mismatches | 8 |

## Behavioral mismatches

- `core/runtime/__init__.py` — barrel_export_mismatch:['SemanticExecutionGraph', 'schedule_semantic_tasks', 'track_semantic_state', 'diff_semantic_state', 'reconcile_semantic_state']
- `core/runtime/cluster_state_engine.py` — py=None js=null is not iterable
- `core/runtime/concurrent_runtime_engine.py` — py=None js=ThreadPoolExecutor is not defined
- `core/runtime/distributed_execution_engine.py` — output_or_state_mismatch
- `core/runtime/execution_causality_engine.py` — output_or_state_mismatch
- `core/runtime/execution_graph_reconciliation_engine.py` — py=None js=n is not defined
- `core/runtime/runtime_consistency_engine.py` — py=None js=(left_keys - right_keys) is not iterable
- `core/runtime/runtime_dependency_engine.py` — output_or_state_mismatch
- `core/runtime/runtime_proof_engine.py` — output_or_state_mismatch
- `core/runtime/runtime_reconciliation_engine.py` — py=None js=(left_keys - right_keys) is not iterable
- `core/runtime/runtime_recovery_engine.py` — output_or_state_mismatch
- `core/runtime/runtime_trace_engine.py` — output_or_state_mismatch
- `core/runtime/runtime_transition_engine.py` — py=None js=Class constructor RuntimeStateMachine cannot be invoked without 'new'
- `core/runtime/semantic_dependency_resolver.py` — py=None js=t is not defined
- `core/runtime/semantic_execution_graph.py` — py=None js=Class constructor SemanticExecutionGraph cannot be invoked without 'new'
- `core/runtime/semantic_lock_engine.py` — py=None js=LOCKS.includes is not a function
- `core/runtime/semantic_orchestration_engine.py` — py=None js=runSemanticPipeline is not defined
- `core/runtime/semantic_orchestrator.py` — py=None js=The requested module './runtimeBudgetEngine.js' does not provide an export named 'DEFAULT_RUNTIME_BUDGET'
- `core/runtime/semantic_pipeline_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/runtime/semantic_pipeline_runtime.py` — py=None js=SemanticExecutionGraph is not defined
- `core/runtime/semantic_reconciliation_runtime.py` — output_or_state_mismatch
- `core/runtime/semantic_replay_vm.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/runtime/semantic_scheduler_engine.py` — py=None js=The requested module './runtimeBudgetEngine.js' does not provide an export named 'DEFAULT_RUNTIME_BUDGET'
- `core/runtime/semantic_security_boundary_engine.py` — py=None js=Cannot read properties of null (reading 'some')
- `core/runtime/semantic_snapshot_engine_v2.py` — py=None js=payload.encode is not a function
- `core/runtime/semantic_task_engine.py` — py=None js=s is not defined
- `core/runtime/service_lifecycle_engine.py` — output_or_state_mismatch
- `core/runtime/topology_runtime_convergence_engine.py` — py=None js=n is not defined

## UNTESTED

- `core/runtime/distributed_cache_engine.py` — no_python_functions
- `core/runtime/runtime_budget_engine.py` — no_python_functions
- `core/runtime/runtime_queue_engine.py` — no_python_functions
- `core/runtime/runtime_state_machine_engine.py` — no_python_functions
- `core/runtime/semantic_cache_engine.py` — no_python_functions
- `core/runtime/semantic_diff_engine.py` — no_python_functions
- `core/runtime/semantic_event_bus_engine.py` — no_python_functions
- `core/runtime/semantic_function_registry.py` — no_python_functions
- `core/runtime/semantic_journal_engine.py` — no_python_functions
- `core/runtime/semantic_memory_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
