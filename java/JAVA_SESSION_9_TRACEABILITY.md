# JAVA_SESSION_9_TRACEABILITY

**Phase 1 — every execution API wired end-to-end.** Verified live from repository state.

| API | Python source | Java source (verified present) | vector section | parity test | validator entry | matrix row |
| --- | --- | --- | --- | --- | --- | --- |
| `build_runtime_sandbox` | `core/execution/runtime_sandbox_engine.py:6` | `io.webweavex.execution.ExecutionRuntime#buildRuntimeSandbox` ✓ | `golden_vectors_s9.json → build_runtime_sandbox` (8) | `CrossLanguageParityS9Test#buildRuntimeSandbox` | `MAPPING["build_runtime_sandbox"]` ✓ | ✅ Implemented (parity-proven) |
| `execute_runtime_action` | `core/execution/runtime_execution_engine.py:45` | `…ExecutionRuntime#executeRuntimeAction` ✓ | `execute_runtime_action` (9) | `…#executeRuntimeAction` | ✓ | ✅ |
| `replay_runtime_execution` | `core/execution/runtime_replay_engine.py:6` | `…ExecutionRuntime#replayRuntimeExecution` ✓ | `replay_runtime_execution` (4) | `…#replayRuntimeExecution` | ✓ | ✅ |
| `simulate_runtime_execution` | `core/execution/runtime_simulation_engine.py:10` | `…ExecutionRuntime#simulateRuntimeExecution` ✓ | `simulate_runtime_execution` (4) | `…#simulateRuntimeExecution` | ✓ | ✅ |
| `run_execution_runtime` | `core/execution/runtime_execution_orchestrator.py:42` | `…ExecutionRuntime#runExecutionRuntime` ✓ | `run_execution_runtime` (8) | `…#runExecutionRuntime` | ✓ | ✅ |
| `run_execution_for_extraction` | `core/execution/runtime_execution_orchestrator.py:185` | `…ExecutionRuntime#runExecutionForExtraction` ✓ | `run_execution_for_extraction` (5) | `…#runExecutionForExtraction` | ✓ | ✅ |

## Wiring verification (live counts)

- **Java source:** `grep -c "public static Map<String,Object> <method>"` → all 6 present
  (`buildRuntimeSandbox` has 3 overloads, `executeRuntimeAction` 2; the rest 1 each).
- **Validator MAPPING:** all 6 keys present (`grep -c` = 1 each).
- **Matrix:** all 6 rows marked `Implemented (parity-proven)`; total proven mark count = **37**.
- **Golden file:** `golden_vectors_s9.json` referenced by `CrossLanguageParityS9Test` (3 refs)
  → validator check 8 PASS.

## Supporting engines (ported, not separate manifest APIs)

`ExecutionRuntime` also ports the ~20 sub-engines + execution IR + the runtime-graph IR-merge,
each independently parity-tested via the **engine-level** vector sections
(`apply_runtime_transition`, `build_runtime_policy`, `enforce_runtime_policy`,
`validate_runtime_permissions`, `track_runtime_mutations`, `enqueue/dequeue_runtime_action`,
`schedule_runtime_execution`, `begin/commit_runtime_transaction`, `build_runtime_workers`,
`federate/coordinate_runtime_execution`, `recover_runtime_execution`, `build_runtime_action`,
`build_unified_runtime_graph`).

**No orphan: every in-scope public API traces Python → Java → vector → test → validator →
matrix.**
