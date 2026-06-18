# JAVA_SESSION_11_DEPENDENCY_PROOF

**Phase 1 — `core.workflows` dependency proof (relative-aware, re-run this session).** Result:
**CLEAN — all 7 APIs implementable** (no forbidden dependency, none dropped).

Tracer: `tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

## Whole-cluster closure

| Metric | Value |
| --- | ---: |
| Modules (relative-aware) | 23 |
| Lines | ~1166 |
| Forbidden | **0** |

Non-pure flags are all stdlib (`hashlib`, `base64`, `unicodedata`, `pathlib`).

## Per-API enumeration & classification

| API | entry module | closure | filesystem | network/browser/OCR/bs4/lxml | class |
| --- | --- | ---: | --- | --- | --- |
| `build_runtime_objective` | `objective_engine` | 1 m | no | none | CLEAN |
| `build_workflow_plan` | `workflow_planner_engine` | 2 m | no | none | CLEAN |
| `replay_workflow_runtime` | `workflow_replay_engine` | 1 m | no | none | CLEAN |
| `run_autonomous_workflow` | `workflow_orchestrator` | 23 m | no | none | CLEAN |
| `run_workflow_for_extraction` | `workflow_orchestrator` | 23 m | no (empty memory path) | none | CLEAN |
| `save_workflow_memory` | `workflow_memory_engine` | 4 m | **yes** (write) | none | CLEAN (reuses PyJson/Kaalka) |
| `load_workflow_memory` | `workflow_memory_engine` | 4 m | **yes** (read) | none | CLEAN (reuses PyJsonParse/Kaalka) |

## Import-type analysis

- **Direct/transitive imports:** only `core.workflows.*`, `core.ir.workflow_runtime_ir`,
  `core.crypto.*`, `core.determinism.*`. No `core.evidence`/`core.semantic` (no bs4 barrier).
- **Relative imports:** none reach a forbidden subsystem.
- **Runtime imports:** one lazy `from core.runtime_graph.runtime_graph_engine import
  build_runtime_graph` inside `run_workflow_for_extraction` (`merge_graph` path) — pure, reused
  as `ExecutionRuntime.buildUnifiedRuntimeGraph`.
- **Filesystem:** confined to `workflow_memory_engine` (save/load); the orchestrator invokes it
  **only when `memory_path` AND `memory_key` are supplied** — never in the parity-proven paths.

**No forbidden dependency in any workflow API. Entire cluster implemented; zero new substrate
required** (no sha256 or pyEquals needed — all pure dict/list transforms).
