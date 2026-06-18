# JAVA_SESSION_11_TRACEABILITY

**Phase 2 — every workflow API traced end-to-end.** Verified live.

| API | Python source | Java target | vector section | parity test | validator | matrix |
| --- | --- | --- | --- | --- | --- | --- |
| `build_runtime_objective` | `objective_engine.py:20` | `io.webweavex.workflow.WorkflowRuntime#buildRuntimeObjective` | `build_runtime_objective` | `S11Test#buildRuntimeObjective` | ✓ | ✅ |
| `build_workflow_plan` | `workflow_planner_engine.py:8` | `…#buildWorkflowPlan` | `build_workflow_plan` | `#buildWorkflowPlan` | ✓ | ✅ |
| `run_autonomous_workflow` | `workflow_orchestrator.py:29` | `…#runAutonomousWorkflow` | `run_autonomous_workflow` | `#runAutonomousWorkflow` | ✓ | ✅ |
| `replay_workflow_runtime` | `workflow_replay_engine.py:6` | `…#replayWorkflowRuntime` | `replay_workflow_runtime` | `#replayWorkflowRuntime` | ✓ | ✅ |
| `run_workflow_for_extraction` | `workflow_orchestrator.py:127` | `…#runWorkflowForExtraction` | `run_workflow_for_extraction` | `#runWorkflowForExtraction` | ✓ | ✅ |
| `save_workflow_memory` | `workflow_memory_engine.py:10` | `…#saveWorkflowMemory` | `save_workflow_memory` (file-content) | `#saveWorkflowMemory` | ✓ | ✅ |
| `load_workflow_memory` | `workflow_memory_engine.py:26` | `…#loadWorkflowMemory` | `load_workflow_memory` (+missing) | `#loadWorkflowMemory` | ✓ | ✅ |

## Supporting engines (ported, engine-level parity-tested)

`execute_workflow_plan`, `build_workflow_state`, `navigate_runtime_workflow`,
`build_workflow_transitions`, `build_workflow_dependencies`, `recover_workflow_runtime`,
`align_workflow_runtime`, `align_workflow_semantics`, `federate_workflow_runtime`,
`schedule_workflow_execution`, `build_workflow_runtime_context`, `build_workflow_graph`,
`remember_workflow_runtime` + the workflow IR (`compile`/`to_graph`) — each has a
`golden_vectors_s11.json` section and a `CrossLanguageParityS11Test` factory.

**No orphan: every in-scope public API and supporting engine traces
Python → Java → vector → test → validator → matrix.**
