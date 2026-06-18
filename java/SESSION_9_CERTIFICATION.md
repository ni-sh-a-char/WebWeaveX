# SESSION 9 CERTIFICATION

**Entire `core.execution` family — 6 APIs, ~20 sub-engines, byte-exact.** Branch `java`. Python
canon `origin/python` @ `9625f4a` (2.1.0).

## Phase 0/1/2 — state, surface, revalidation

- [`JAVA_SESSION_9_STATE.md`](JAVA_SESSION_9_STATE.md) — 37 proven / 91 remaining (machine-derived).
- [`JAVA_PARITY_SURFACE_MAP.md`](JAVA_PARITY_SURFACE_MAP.md) — families; **every remaining clean
  family now needs zero new substrate**.
- [`JAVA_SESSION_9_EXECUTION_AUDIT.md`](JAVA_SESSION_9_EXECUTION_AUDIT.md) — fresh relative-aware
  trace: 26 modules / 0 forbidden / FS checkpoint imported-not-called → **CLEAN, no STOP**.

## Implemented APIs (6) — full family, no cherry-pick

| API | Java | Python canon |
| --- | --- | --- |
| `build_runtime_sandbox` | `io.webweavex.execution.ExecutionRuntime#buildRuntimeSandbox` | `runtime_sandbox_engine` |
| `execute_runtime_action` | `…#executeRuntimeAction` | `runtime_execution_engine` (+ action/permissions/policy) |
| `replay_runtime_execution` | `…#replayRuntimeExecution` | `runtime_replay_engine` |
| `simulate_runtime_execution` | `…#simulateRuntimeExecution` | `runtime_simulation_engine` |
| `run_execution_runtime` | `…#runExecutionRuntime` | `runtime_execution_orchestrator` (fans to ~18 engines + IR) |
| `run_execution_for_extraction` | `…#runExecutionForExtraction` | orchestrator + IR-to-graph + unified-graph merge |

All ~20 sub-engines ported (sandbox/action/permissions/policy/mutation/transaction/transition/
queue/scheduler/worker/federation/coordination/recovery/rollback/state/replay/simulation + the
execution IR + the `runtime_graph_engine` IR-merge). No stubs/TODOs. The FS checkpoint path is
not exercised (empty memory path) — faithfully mirrored.

## Parity proof

- `tools/gen_java_parity_vectors_s9.py` → `golden_vectors_s9.json` — **89 vectors**: 38 top-level
  (empty/unicode/normalization/malformed/nested/ordering/replay/mutation/regression/boundary)
  + 51 engine-level (Python-oracle parity for every internal engine + branch:
  transitions, policy, permissions, mutations, queue, scheduler, transaction, workers,
  federation, coordination, recovery, action IDs, unified-graph merge).
- `CrossLanguageParityS9Test` — **89/89 byte-exact** (`stable_serialize` + `compute_kaalka_hash`).

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 31 | **37** |
| Remaining (of 128) | 97 | **91** |
| Total tests | 365 | **454** |
| Instruction coverage | 95.68% | **95.88%** (ExecutionRuntime 96.5%) |
| `PROVEN_FLOOR` | 31 | **37** |

## Governance & quality gates

Validator **PASS 37/128** (MAPPING +6; `execution` added to matrix PACKAGES). Matrix regenerated.
Manifest unchanged. Coverage increased; all tests parity-backed (Python oracle, incl. the
engine-level suite) — no synthetic/self-consistency tests. `mvn verify` BUILD SUCCESS (454/0/0).

## Phase 4/5/6 — leverage, blockers, extraction

- [`JAVA_SUBSTRATE_LEVERAGE.md`](JAVA_SUBSTRATE_LEVERAGE.md) — remaining clean surface (~46 APIs)
  needs **zero** new substrate.
- [`JAVA_BLOCKER_HIERARCHY.md`](JAVA_BLOCKER_HIERARCHY.md) — #1 leverage = upstream bs4-decouple
  (~26 APIs).
- [`JAVA_EXTRACTION_ROADMAP.md`](JAVA_EXTRACTION_ROADMAP.md) — import-time vs behavioral split.

## Next

[`JAVA_SESSION_10_PLAN.md`](JAVA_SESSION_10_PLAN.md): `core.synchronization` family (6 APIs, zero
substrate). The mission continues — 37/128.
