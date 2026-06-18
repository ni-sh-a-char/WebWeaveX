# JAVA_SESSION_13_DEPENDENCY_PROOF

**Phase 1 — `core.causality` dependency proof (relative-aware, re-run this session).**
Result: **CLEAN — all 5 APIs implementable** (0 forbidden, none dropped).

Tracer: `tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

## Whole-cluster closure

| Metric | Value |
| --- | ---: |
| Modules (relative-aware) | 25 |
| Lines | ~1360 |
| Forbidden | **0** |

Non-pure flags are stdlib only (`pathlib` in the memory engine; `base64`/`hashlib`/`unicodedata`
in the shared crypto/determinism substrate — no causality engine uses `hashlib` directly).

## Per-API classification

| API | entry module | closure | filesystem | network/browser/OCR/bs4/lxml | class |
| --- | --- | ---: | --- | --- | --- |
| `run_causality_runtime` | `causality_orchestrator` | 25 m | no | none | CLEAN |
| `replay_causal_runtime` | `causal_replay_engine` | 1 m | no | none | CLEAN |
| `run_causality_for_extraction` | `causality_orchestrator` | 25 m | no (empty memory path) | none | CLEAN |
| `save_causal_memory` | `causal_memory_engine` | 4 m | **yes** (write) | none | CLEAN (reuses PyJson/Kaalka) |
| `load_causal_memory` | `causal_memory_engine` | 4 m | **yes** (read) | none | CLEAN (reuses PyJsonParse/Kaalka) |

## Import-type analysis

- **Direct/transitive:** only `core.causality.*`, `core.ir.causal_runtime_ir`, `core.crypto.*`,
  `core.determinism.*`. No `core.evidence`/`core.semantic` (no bs4 barrier).
- **Relative imports:** none reach a forbidden subsystem.
- **Runtime imports:** one lazy `from core.runtime_graph.runtime_graph_engine import
  build_runtime_graph` inside `run_causality_for_extraction` (`merge_graph`) — reused as
  `ExecutionRuntime.buildUnifiedRuntimeGraph`.
- **Filesystem:** confined to `causal_memory_engine`; the orchestrator invokes it only with a
  memory path+key — never in the parity-proven paths.

**No forbidden dependency. Entire cluster implemented. ZERO new substrate** (no sha256/pyEquals —
all pure event/dict/list transforms).
