# JAVA_SESSION_14_TRACEABILITY

**Phase 2 — every certified API traced end-to-end.** Verified live.

| API | Python source | Java target | vector section | parity test | validator | matrix |
| --- | --- | --- | --- | --- | --- | --- |
| `build_stream_timeline` | `streaming/stream_replay_engine.py:30` | `io.webweavex.streaming.StreamingRuntime#buildStreamTimeline` | `build_stream_timeline` | `S14Test#buildStreamTimeline` | ✓ | ✅ |
| `replay_stream_events` | `streaming/stream_replay_engine.py:8` | `…#replayStreamEvents` | `replay_stream_events` | `#replayStreamEvents` | ✓ | ✅ |
| `run_live_runtime` | `connectors/live_runtime_orchestrator.py:24` | `…#runLiveRuntime` | `run_live_runtime` (projection) | `#runLiveRuntime` | ✓ | ✅ |
| `save_live_runtime` | `connectors/live_runtime_memory_engine.py:10` | `…#saveLiveRuntime` | `save_live_runtime` (file-content) | `#saveLiveRuntime` | ✓ | ✅ |
| `load_live_runtime` | `connectors/live_runtime_memory_engine.py:26` | `…#loadLiveRuntime` | `load_live_runtime` (+missing) | `#loadLiveRuntime` | ✓ | ✅ |

## Supporting engines (ported, engine-level parity-tested)

`extract_filesystem_runtime` (snapshot + null-FS-walk + missing-dir), `extract_cicd_runtime`,
`build_live_topology_graph`, `compile_live_runtime_ir`, `live_runtime_ir_to_graph`,
`remember_live_runtime` — each has a `golden_vectors_s14.json` section and a
`CrossLanguageParityS14Test` factory. The 7 reused connector engines are exercised transitively
through `run_live_runtime`'s projection vectors.

**No orphan: every certified API + supporting engine traces
Python → Java → vector → test → validator → matrix.**
