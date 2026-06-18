# JAVA_SESSION_13_TRACEABILITY

**Phase 2 — every causality API traced end-to-end.** Verified live.

| API | Python source | Java target | vector section | parity test | validator | matrix |
| --- | --- | --- | --- | --- | --- | --- |
| `run_causality_runtime` | `causality_orchestrator.py:99` | `io.webweavex.causality.CausalityRuntime#runCausalityRuntime` | `run_causality_runtime` | `S13Test#runCausalityRuntime` | ✓ | ✅ |
| `replay_causal_runtime` | `causal_replay_engine.py:6` | `…#replayCausalRuntime` | `replay_causal_runtime` | `#replayCausalRuntime` | ✓ | ✅ |
| `run_causality_for_extraction` | `causality_orchestrator.py:200` | `…#runCausalityForExtraction` | `run_causality_for_extraction` | `#runCausalityForExtraction` | ✓ | ✅ |
| `save_causal_memory` | `causal_memory_engine.py:10` | `…#saveCausalMemory` | `save_causal_memory` (file-content) | `#saveCausalMemory` | ✓ | ✅ |
| `load_causal_memory` | `causal_memory_engine.py:26` | `…#loadCausalMemory` | `load_causal_memory` (+missing) | `#loadCausalMemory` | ✓ | ✅ |

## Supporting engines (ported, engine-level parity-tested)

`build_runtime_causality`, `build_event_chain`, `align_cross_runtime_events`,
`build_runtime_dependencies`, `build_workflow_propagation`, `build_causal_graph`,
`build_state_transitions`, `build_runtime_sequence`, `build_runtime_timeline`,
`correlate_runtime_mutations`, `build_distributed_causality`, `bridge_browser_native_runtime`,
`bridge_electron_terminal_runtime`, `track_notification_causality`, `track_process_causality`,
`recover_causal_runtime`, `remember_causal_runtime` + the causal IR — each has a
`golden_vectors_s13.json` section and a `CrossLanguageParityS13Test` factory.

**No orphan: every in-scope public API and supporting engine traces
Python → Java → vector → test → validator → matrix.**
