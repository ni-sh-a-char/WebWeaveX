# JAVA_SESSION_12_DEPENDENCY_PROOF

**Phase 1 — `core.evolution_runtime` dependency proof (relative-aware, re-run this session).**
Result: **CLEAN — all 6 APIs implementable** (0 forbidden, none dropped).

Tracer: `tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

## Whole-cluster closure

| Metric | Value |
| --- | ---: |
| Modules (relative-aware) | 25 |
| Lines | ~1237 |
| Forbidden | **0** |

Non-pure flags are stdlib (`hashlib`, `base64`, `unicodedata`, `pathlib`).

## Per-API classification

| API | entry module | closure | filesystem | network/browser/OCR/bs4/lxml | class |
| --- | --- | ---: | --- | --- | --- |
| `build_runtime_evolution` | `runtime_evolution_engine` | 1 m | no | none | CLEAN |
| `evolve_selector_runtime` | `selector_evolution_engine` | 1 m | no | none | CLEAN |
| `run_evolution_runtime` | `runtime_evolution_orchestrator` | 25 m | no | none | CLEAN |
| `run_evolution_for_extraction` | `runtime_evolution_orchestrator` | 25 m | no (empty memory path) | none | CLEAN |
| `save_evolution_runtime` | `runtime_memory_engine` | 4 m | **yes** (write) | none | CLEAN (reuses PyJson/Kaalka) |
| `load_evolution_runtime` | `runtime_memory_engine` | 4 m | **yes** (read) | none | CLEAN (reuses PyJsonParse/Kaalka) |

## Import-type analysis

- **Direct/transitive:** only `core.evolution_runtime.*`, `core.ir.evolution_runtime_ir`,
  `core.crypto.*`, `core.determinism.*`. No `core.evidence`/`core.semantic` (no bs4 barrier).
- **Relative imports:** none reach a forbidden subsystem.
- **Runtime imports:** one lazy `from core.runtime_graph.runtime_graph_engine import
  build_runtime_graph` inside `run_evolution_for_extraction` (`merge_graph`) — reused as
  `ExecutionRuntime.buildUnifiedRuntimeGraph`.
- **Filesystem:** confined to `runtime_memory_engine`; orchestrator invokes it only with a
  memory path+key — never in the parity-proven paths.

**No forbidden dependency. Entire cluster implemented.** Only new helper: `sha256hex32` (already
present in Sync/Execution). No other new substrate.
