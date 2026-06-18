# JAVA_SESSION_11_CERTIFICATION

**Entire `core.workflows` family — 7 APIs, ~15 sub-engines, byte-exact. Milestone: 50/128.**
Branch `java`. Python canon `origin/python` @ `9625f4a` (2.1.0).

## Implemented APIs (7) — full family, no cherry-pick

| API | Java | Python canon |
| --- | --- | --- |
| `build_runtime_objective` | `io.webweavex.workflow.WorkflowRuntime#buildRuntimeObjective` | `objective_engine` |
| `build_workflow_plan` | `…#buildWorkflowPlan` | `workflow_planner_engine` |
| `run_autonomous_workflow` | `…#runAutonomousWorkflow` | `workflow_orchestrator` (fans to ~15 engines + IR) |
| `replay_workflow_runtime` | `…#replayWorkflowRuntime` | `workflow_replay_engine` |
| `run_workflow_for_extraction` | `…#runWorkflowForExtraction` | orchestrator + IR-to-graph + unified-graph merge |
| `save_workflow_memory` | `…#saveWorkflowMemory` | `workflow_memory_engine` (FS + Kaalka + json.dumps) |
| `load_workflow_memory` | `…#loadWorkflowMemory` | `workflow_memory_engine` (FS + Kaalka + json.loads) |

All ~15 sub-engines + the workflow IR + the reused runtime-graph IR-merge ported. **Zero new
substrate** — reuses StableSerialize, Kaalka, PyJson, PyJsonParse, PyRepr, Normalization,
`ExecutionRuntime.buildUnifiedRuntimeGraph`. No stubs.

## Proofs

- **Dependency:** [`JAVA_SESSION_11_DEPENDENCY_PROOF.md`](JAVA_SESSION_11_DEPENDENCY_PROOF.md) — 23 modules / 0 forbidden.
- **Traceability:** [`JAVA_SESSION_11_TRACEABILITY.md`](JAVA_SESSION_11_TRACEABILITY.md) — no orphan.
- **Parity:** [`JAVA_SESSION_11_PARITY_PROOF.md`](JAVA_SESSION_11_PARITY_PROOF.md) — **50/50** byte-exact (50 vectors / 20 sections, incl. 13 engine-level).
- **Coverage:** [`JAVA_SESSION_11_COVERAGE_PROOF.md`](JAVA_SESSION_11_COVERAGE_PROOF.md) — **96.13 % → 96.29 %** (WorkflowRuntime 97.1 %).
- **Governance:** [`JAVA_SESSION_11_GOVERNANCE_AUDIT.md`](JAVA_SESSION_11_GOVERNANCE_AUDIT.md) — validator PASS 50/128.
- **Blocker:** [`JAVA_SESSION_11_BLOCKER_AUDIT.md`](JAVA_SESSION_11_BLOCKER_AUDIT.md) — no workflow blocker.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 43 | **50** |
| Remaining (of 128) | 85 | **78** |
| Total tests | 503 | **553** |
| Instruction coverage | 96.13 % | **96.29 %** |
| `PROVEN_FLOOR` | 43 | **50** |

`mvn clean verify` BUILD SUCCESS (553/0/0). Manifest unchanged. All tests parity-backed.

## Next

[`JAVA_SESSION_12_PLAN.md`](JAVA_SESSION_12_PLAN.md): `core.evolution_runtime` (6 APIs, zero
substrate). Mission active — 50/128.
