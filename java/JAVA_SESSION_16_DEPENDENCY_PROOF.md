# JAVA_SESSION_16_DEPENDENCY_PROOF

**Phase 1 — relative-aware dependency proof.** Tracer `tools/trace_imports_s5_relative.py`.
Canon `origin/python` @ `9625f4a`.

| API | def module | closure | forbidden | class |
| --- | --- | ---: | ---: | --- |
| `run_reconstruction_runtime` | `reconstruction/runtime_reconstruction_orchestrator` | 24 m / 1407 L | 0 | **CLEAN** |
| `run_reconstruction_for_extraction` | `reconstruction/runtime_reconstruction_orchestrator` | 24 m / 1407 L | 0 | **CLEAN** |

Closure fans out to ~18 sub-engines + the reconstruction IR + `core.crypto`/`core.determinism`.
No `core.evidence`/`core.semantic` (no bs4 barrier). One lazy runtime import
(`core.runtime_graph.runtime_graph_engine.build_runtime_graph`) in `*_for_extraction`'s
`merge_graph` path — reused as `ExecutionRuntime.buildUnifiedRuntimeGraph`. FS confined to the
snapshot engine (save/load), invoked only with a memory path+key. **Serializable output** (no
self-reference) → direct byte-exact parity. Zero new substrate.
