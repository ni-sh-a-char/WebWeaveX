# JAVA_SESSION_10_DEPENDENCY_PROOF

**Phase 1 — `core.synchronization` dependency proof (relative-aware, re-run this session).**
Result: **CLEAN — all 6 APIs implementable** (no forbidden dependency).

Tracer: `tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

## Whole-cluster closure

| Metric | Value |
| --- | ---: |
| Modules (relative-aware) | 25 |
| Lines | ~1262 |
| Forbidden | **0** |

Non-pure flags are all stdlib (`hashlib`, `base64`, `unicodedata`, `pathlib`).

## Per-API enumeration & resolution

| API | entry module | closure | filesystem | network/browser/OCR/bs4/lxml | verdict |
| --- | --- | ---: | --- | --- | --- |
| `build_runtime_delta` | `runtime_delta_engine` | 1 m | no | none | CLEAN |
| `replay_synchronized_runtime` | `runtime_replay_engine` | 1 m | no | none | CLEAN |
| `run_synchronized_runtime` | `runtime_sync_orchestrator` | 25 m | no | none | CLEAN |
| `run_sync_for_extraction` | `runtime_sync_orchestrator` | 25 m | no (empty memory path) | none | CLEAN |
| `save_sync_memory` | `runtime_sync_memory_engine` | 4 m | **yes** (write) | none | CLEAN (FS, reuses PyJson/Kaalka) |
| `load_sync_memory` | `runtime_sync_memory_engine` | 4 m | **yes** (read) | none | CLEAN (FS, reuses PyJsonParse/Kaalka) |

## Import-type analysis

- **Direct/transitive imports:** only `core.synchronization.*`, `core.ir.synchronization_runtime_ir`,
  `core.crypto.*`, `core.determinism.*`.
- **Relative imports:** none reach a forbidden subsystem (no `core.evidence`/`core.semantic`).
- **Runtime imports:** one lazy `from core.runtime_graph.runtime_graph_engine import
  build_runtime_graph` inside `run_sync_for_extraction` (`merge_graph` path) — pure, already
  ported as `ExecutionRuntime.buildUnifiedRuntimeGraph`.
- **Filesystem:** confined to `runtime_sync_memory_engine` (save/load); the orchestrator invokes
  it **only when `memory_path` AND `memory_key` are supplied** — never in the parity-proven
  paths (vectored with empty path; save/load tested directly against a temp dir).

**No forbidden dependency in any synchronization API. Entire cluster proceeds.** No API was
dropped.
