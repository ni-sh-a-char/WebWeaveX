# WebWeaveX API Reference

Generated from `PARITY_MANIFEST.json` by `tools/gen_api_reference.py` — do not edit by hand.

**105 Complete · 18 Partial · 5 Deferred · 0 Missing** (see CERTIFICATION.md for what each class means and how it is proven).

Naming: Python/JS export `snake_case`/`camelCase` per language convention; the Dart symbol is listed explicitly.

## Complete (105)

Parity-certified 3-way (Python == JavaScript == Dart) by executed proof.

| API | Dart symbol | Proof |
|---|---|---|
| `RuntimeKernel` | `RuntimeKernel` | VECTOR |
| `UniversalInput` | `UniversalInput` | VECTOR |
| `__version__` | `version` | TEST_ONLY |
| `authenticate_runtime` | `authenticateRuntime` | VECTOR |
| `build_browser_identity` | `buildBrowserIdentity` | EXECUTABLE |
| `build_interaction_graph` | `buildInteractionGraph` | VECTOR |
| `build_runtime_delta` | `buildRuntimeDelta` | VECTOR |
| `build_runtime_evolution` | `buildRuntimeEvolution` | VECTOR |
| `build_runtime_graph` | `buildRuntimeGraph` | CORE_VECTOR |
| `build_runtime_memory` | `buildRuntimeMemory` | EXECUTABLE |
| `build_runtime_objective` | `buildRuntimeObjective` | VECTOR |
| `build_runtime_sandbox` | `buildRuntimeSandbox` | VECTOR |
| `build_stream_timeline` | `buildStreamTimeline` | VECTOR |
| `build_workflow_plan` | `buildWorkflowPlan` | VECTOR |
| `clone_runtime_environment` | `cloneRuntimeEnvironment` | VECTOR |
| `compile_document` | `compileDocument` | — |
| `compile_repository` | `compileRepository` | — |
| `compile_unified_runtime_ir` | `compileUnifiedRuntimeIr` | VECTOR |
| `compute_global_runtime_fingerprint` | `computeGlobalRuntimeFingerprint` | EXECUTABLE |
| `compute_kaalka_hash` | `computeKaalkaHash` | EXECUTABLE |
| `decrypt_session_state` | `decryptSessionState` | VECTOR |
| `decrypt_value` | `decryptValue` | CORE_VECTOR |
| `encrypt_session_state` | `encryptSessionState` | VECTOR |
| `encrypt_value` | `encryptValue` | CORE_VECTOR |
| `evolve_selector_runtime` | `evolveSelectorRuntime` | VECTOR |
| `execute_runtime_action` | `executeRuntimeAction` | VECTOR |
| `execute_runtime_objective` | `executeRuntimeObjective` | EXECUTABLE |
| `extract_api_runtime` | `extractApiRuntime` | VECTOR |
| `extract_container_runtime` | `extractContainerRuntime` | EXECUTABLE |
| `extract_database_runtime` | `extractDatabaseRuntime` | EXECUTABLE |
| `extract_ide_runtime` | `extractIdeRuntime` | EXECUTABLE |
| `extract_kubernetes_runtime` | `extractKubernetesRuntime` | EXECUTABLE |
| `extract_multimodal` | `extractMultimodal` | — |
| `extract_paginated_content` | `extractPaginatedContent` | — |
| `extract_runtime_streams` | `extractRuntimeStreams` | VECTOR |
| `extract_telemetry_runtime` | `extractTelemetryRuntime` | VECTOR |
| `fabricate_runtime_reality` | `fabricateRuntimeReality` | VECTOR |
| `fingerprint` | `fingerprint` | VECTOR |
| `get_runtime_kernel` | `getRuntimeKernel` | EXECUTABLE |
| `ingest_input` | `ingestInput` | — |
| `load_adaptive_memory` | `loadAdaptiveMemory` | ROUNDTRIP |
| `load_application_memory` | `loadApplicationMemory` | ROUNDTRIP |
| `load_browser_identity` | `loadBrowserIdentity` | ROUNDTRIP |
| `load_causal_memory` | `loadCausalMemory` | ROUNDTRIP |
| `load_distributed_checkpoint` | `loadDistributedCheckpoint` | ROUNDTRIP |
| `load_encrypted_session` | `loadEncryptedSession` | ROUNDTRIP |
| `load_evolution_runtime` | `loadEvolutionRuntime` | ROUNDTRIP |
| `load_live_runtime` | `loadLiveRuntime` | ROUNDTRIP |
| `load_native_runtime` | `loadNativeRuntime` | ROUNDTRIP |
| `load_runtime_memory` | `loadRuntimeMemory` | ROUNDTRIP |
| `load_semantic_memory` | `loadSemanticMemory` | ROUNDTRIP |
| `load_sync_memory` | `loadSyncMemory` | ROUNDTRIP |
| `load_workflow_memory` | `loadWorkflowMemory` | ROUNDTRIP |
| `query_documents` | `queryDocuments` | — |
| `query_graph` | `queryGraph` | VECTOR |
| `query_knowledge` | `queryKnowledge` | VECTOR |
| `query_repo` | `queryRepo` | VECTOR |
| `query_repository` | `queryRepository` | — |
| `query_runtime_graph` | `queryRuntimeGraph` | EXECUTABLE |
| `query_runtime_memory` | `queryRuntimeMemory` | EXECUTABLE |
| `query_semantics` | `querySemantics` | — |
| `reason_semantically` | `reasonSemantically` | — |
| `reconstruct_runtime` | `reconstructRuntime` | EXECUTABLE |
| `recover_modal_runtime` | `recoverModalRuntime` | — |
| `replay_causal_runtime` | `replayCausalRuntime` | VECTOR |
| `replay_runtime_execution` | `replayRuntimeExecution` | VECTOR |
| `replay_semantic_runtime` | `replaySemanticRuntime` | VECTOR |
| `replay_stream_events` | `replayStreamEvents` | VECTOR |
| `replay_synchronized_runtime` | `replaySynchronizedRuntime` | VECTOR |
| `replay_workflow_runtime` | `replayWorkflowRuntime` | VECTOR |
| `run_application_cognition` | `runApplicationCognition` | — |
| `run_autonomous_workflow` | `runAutonomousWorkflow` | VECTOR |
| `run_causality_for_extraction` | `runCausalityForExtraction` | VECTOR |
| `run_causality_runtime` | `runCausalityRuntime` | VECTOR |
| `run_evolution_for_extraction` | `runEvolutionForExtraction` | VECTOR |
| `run_evolution_runtime` | `runEvolutionRuntime` | VECTOR |
| `run_execution_for_extraction` | `runExecutionForExtraction` | VECTOR |
| `run_execution_runtime` | `runExecutionRuntime` | VECTOR |
| `run_memory_for_extraction` | `runMemoryForExtraction` | VECTOR |
| `run_reconstruction_for_extraction` | `runReconstructionForExtraction` | VECTOR |
| `run_reconstruction_runtime` | `runReconstructionRuntime` | VECTOR |
| `run_runtime_memory` | `runRuntimeMemory` | VECTOR |
| `run_semantic_for_extraction` | `runSemanticForExtraction` | VECTOR |
| `run_semantic_runtime` | `runSemanticRuntime` | VECTOR |
| `run_sync_for_extraction` | `runSyncForExtraction` | VECTOR |
| `run_synchronized_runtime` | `runSynchronizedRuntime` | VECTOR |
| `run_workflow_for_extraction` | `runWorkflowForExtraction` | VECTOR |
| `save_adaptive_memory` | `saveAdaptiveMemory` | ROUNDTRIP |
| `save_application_memory` | `saveApplicationMemory` | ROUNDTRIP |
| `save_browser_identity` | `saveBrowserIdentity` | ROUNDTRIP |
| `save_causal_memory` | `saveCausalMemory` | ROUNDTRIP |
| `save_distributed_checkpoint` | `saveDistributedCheckpoint` | ROUNDTRIP |
| `save_encrypted_session` | `saveEncryptedSession` | ROUNDTRIP |
| `save_evolution_runtime` | `saveEvolutionRuntime` | ROUNDTRIP |
| `save_live_runtime` | `saveLiveRuntime` | ROUNDTRIP |
| `save_native_runtime` | `saveNativeRuntime` | ROUNDTRIP |
| `save_runtime_memory` | `saveRuntimeMemory` | ROUNDTRIP |
| `save_semantic_memory` | `saveSemanticMemory` | ROUNDTRIP |
| `save_sync_memory` | `saveSyncMemory` | ROUNDTRIP |
| `save_workflow_memory` | `saveWorkflowMemory` | ROUNDTRIP |
| `search_runtime_memory` | `searchRuntimeMemory` | VECTOR |
| `simulate_runtime_execution` | `simulateRuntimeExecution` | VECTOR |
| `validate_reconstructed_runtime` | `validateReconstructedRuntime` | VECTOR |
| `validate_replay_equivalence` | `validateReplayEquivalence` | EXECUTABLE |
| `version` | `version` | TEST_ONLY |

## Partial (18)

Deterministic core certified; a documented network or live-browser sub-path is excluded by design.

| API | Dart symbol | Proof |
|---|---|---|
| `analyze` | `analyze` | NONE |
| `crawl` | `—` | NONE |
| `crawl_async` | `—` | NONE |
| `extract` | `—` | NONE |
| `extract_async` | `—` | NONE |
| `extract_docs` | `—` | NONE |
| `extract_document_runtime` | `—` | NONE |
| `extract_recursive` | `—` | NONE |
| `extract_repo` | `—` | NONE |
| `extract_repository` | `—` | NONE |
| `extract_web` | `—` | NONE |
| `heal_selector` | `healSelector` | NONE |
| `replay_interactions` | `replayInteractions` | NONE |
| `run_autonomous_extraction` | `—` | NONE |
| `run_canonical_pipeline` | `runCanonicalPipeline` | NONE |
| `run_live_runtime` | `runLiveRuntime` | NONE |
| `stream_extract` | `—` | NONE |
| `universal_extract` | `—` | NONE |

## Deferred (5)

Platform-bound (live page / OS coupling); not part of the portable surface.

| API | Dart symbol | Proof |
|---|---|---|
| `capture_dom_mutations` | `—` | NONE |
| `capture_websocket_frames` | `—` | NONE |
| `extract_infinite_scroll` | `—` | NONE |
| `extract_native` | `—` | NONE |
| `run_native_cognition` | `—` | NONE |
