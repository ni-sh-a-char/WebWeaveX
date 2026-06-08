# FINAL PUBLIC API CERTIFICATION

**Measured:** 2026-06-08T08:54:34.519575+00:00

**Status:** PASS

Evidence: Python `__all__` from `origin/python:webweavex/__init__.py`; JavaScript surface = runtime `Object.keys()` of the built `dist/index.js`.

| Check | Result | Detail |
|-------|--------|--------|
| Python public names | 128 | from `__all__` |
| JavaScript runtime exports | 229 | from dist import |
| Coverage (every Python name has a JS export) | PASS | 128/128 |
| Missing exports | PASS | none |
| Double-ownership (name declared by >1 source) | PASS | none |
| Star-import conflict (connectors vs publicApi) | PASS | none |

## Spec-conformance notes

- `buildRuntimeGraph` / `queryRuntimeGraph` resolve to the spec ports `src/runtime_graph/*` (`core.runtime_graph`, list-of-IRs / `(graph, query)`), matching the Python public signatures. The dict-source helpers in `src/graph/runtimeGraph.ts` are JS-internal (pipeline) and are NOT the public exports.
- `UniversalInput` is exported as a runtime class value (not type-only).

## Full mapping (Python public name -> JavaScript export)

| Python | JavaScript |
|--------|------------|
| `RuntimeKernel` | `RuntimeKernel` |
| `UniversalInput` | `UniversalInput` |
| `__version__` | `VERSION` |
| `analyze` | `analyze` |
| `authenticate_runtime` | `authenticateRuntime` |
| `build_browser_identity` | `buildBrowserIdentity` |
| `build_interaction_graph` | `buildInteractionGraph` |
| `build_runtime_delta` | `buildRuntimeDelta` |
| `build_runtime_evolution` | `buildRuntimeEvolution` |
| `build_runtime_graph` | `buildRuntimeGraph` |
| `build_runtime_memory` | `buildRuntimeMemory` |
| `build_runtime_objective` | `buildRuntimeObjective` |
| `build_runtime_sandbox` | `buildRuntimeSandbox` |
| `build_stream_timeline` | `buildStreamTimeline` |
| `build_workflow_plan` | `buildWorkflowPlan` |
| `capture_dom_mutations` | `captureDomMutations` |
| `capture_websocket_frames` | `captureWebsocketFrames` |
| `clone_runtime_environment` | `cloneRuntimeEnvironment` |
| `compile_document` | `compileDocument` |
| `compile_repository` | `compileRepository` |
| `compile_unified_runtime_ir` | `compileUnifiedRuntimeIr` |
| `compute_global_runtime_fingerprint` | `computeGlobalRuntimeFingerprint` |
| `compute_kaalka_hash` | `computeKaalkaHash` |
| `crawl` | `crawl` |
| `crawl_async` | `crawlAsync` |
| `decrypt_session_state` | `decryptSessionState` |
| `decrypt_value` | `decryptValue` |
| `encrypt_session_state` | `encryptSessionState` |
| `encrypt_value` | `encryptValue` |
| `evolve_selector_runtime` | `evolveSelectorRuntime` |
| `execute_runtime_action` | `executeRuntimeAction` |
| `execute_runtime_objective` | `executeRuntimeObjective` |
| `extract` | `extract` |
| `extract_api_runtime` | `extractApiRuntime` |
| `extract_async` | `extractAsync` |
| `extract_container_runtime` | `extractContainerRuntime` |
| `extract_database_runtime` | `extractDatabaseRuntime` |
| `extract_docs` | `extractDocs` |
| `extract_document_runtime` | `extractDocumentRuntime` |
| `extract_ide_runtime` | `extractIdeRuntime` |
| `extract_infinite_scroll` | `extractInfiniteScroll` |
| `extract_kubernetes_runtime` | `extractKubernetesRuntime` |
| `extract_multimodal` | `extractMultimodal` |
| `extract_native` | `extractNative` |
| `extract_paginated_content` | `extractPaginatedContent` |
| `extract_recursive` | `extractRecursive` |
| `extract_repo` | `extractRepo` |
| `extract_repository` | `extractRepository` |
| `extract_runtime_streams` | `extractRuntimeStreams` |
| `extract_telemetry_runtime` | `extractTelemetryRuntime` |
| `extract_web` | `extractWeb` |
| `fabricate_runtime_reality` | `fabricateRuntimeReality` |
| `fingerprint` | `fingerprint` |
| `get_runtime_kernel` | `getRuntimeKernel` |
| `heal_selector` | `healSelector` |
| `ingest_input` | `ingestInput` |
| `load_adaptive_memory` | `loadAdaptiveMemory` |
| `load_application_memory` | `loadApplicationMemory` |
| `load_browser_identity` | `loadBrowserIdentity` |
| `load_causal_memory` | `loadCausalMemory` |
| `load_distributed_checkpoint` | `loadDistributedCheckpoint` |
| `load_encrypted_session` | `loadEncryptedSession` |
| `load_evolution_runtime` | `loadEvolutionRuntime` |
| `load_live_runtime` | `loadLiveRuntime` |
| `load_native_runtime` | `loadNativeRuntime` |
| `load_runtime_memory` | `loadRuntimeMemory` |
| `load_semantic_memory` | `loadSemanticMemory` |
| `load_sync_memory` | `loadSyncMemory` |
| `load_workflow_memory` | `loadWorkflowMemory` |
| `query_documents` | `queryDocuments` |
| `query_graph` | `queryGraph` |
| `query_knowledge` | `queryKnowledge` |
| `query_repo` | `queryRepo` |
| `query_repository` | `queryRepository` |
| `query_runtime_graph` | `queryRuntimeGraph` |
| `query_runtime_memory` | `queryRuntimeMemory` |
| `query_semantics` | `querySemantics` |
| `reason_semantically` | `reasonSemantically` |
| `reconstruct_runtime` | `reconstructRuntime` |
| `recover_modal_runtime` | `recoverModalRuntime` |
| `replay_causal_runtime` | `replayCausalRuntime` |
| `replay_interactions` | `replayInteractions` |
| `replay_runtime_execution` | `replayRuntimeExecution` |
| `replay_semantic_runtime` | `replaySemanticRuntime` |
| `replay_stream_events` | `replayStreamEvents` |
| `replay_synchronized_runtime` | `replaySynchronizedRuntime` |
| `replay_workflow_runtime` | `replayWorkflowRuntime` |
| `run_application_cognition` | `runApplicationCognition` |
| `run_autonomous_extraction` | `runAutonomousExtraction` |
| `run_autonomous_workflow` | `runAutonomousWorkflow` |
| `run_canonical_pipeline` | `runCanonicalPipeline` |
| `run_causality_for_extraction` | `runCausalityForExtraction` |
| `run_causality_runtime` | `runCausalityRuntime` |
| `run_evolution_for_extraction` | `runEvolutionForExtraction` |
| `run_evolution_runtime` | `runEvolutionRuntime` |
| `run_execution_for_extraction` | `runExecutionForExtraction` |
| `run_execution_runtime` | `runExecutionRuntime` |
| `run_live_runtime` | `runLiveRuntime` |
| `run_memory_for_extraction` | `runMemoryForExtraction` |
| `run_native_cognition` | `runNativeCognition` |
| `run_reconstruction_for_extraction` | `runReconstructionForExtraction` |
| `run_reconstruction_runtime` | `runReconstructionRuntime` |
| `run_runtime_memory` | `runRuntimeMemory` |
| `run_semantic_for_extraction` | `runSemanticForExtraction` |
| `run_semantic_runtime` | `runSemanticRuntime` |
| `run_sync_for_extraction` | `runSyncForExtraction` |
| `run_synchronized_runtime` | `runSynchronizedRuntime` |
| `run_workflow_for_extraction` | `runWorkflowForExtraction` |
| `save_adaptive_memory` | `saveAdaptiveMemory` |
| `save_application_memory` | `saveApplicationMemory` |
| `save_browser_identity` | `saveBrowserIdentity` |
| `save_causal_memory` | `saveCausalMemory` |
| `save_distributed_checkpoint` | `saveDistributedCheckpoint` |
| `save_encrypted_session` | `saveEncryptedSession` |
| `save_evolution_runtime` | `saveEvolutionRuntime` |
| `save_live_runtime` | `saveLiveRuntime` |
| `save_native_runtime` | `saveNativeRuntime` |
| `save_runtime_memory` | `saveRuntimeMemory` |
| `save_semantic_memory` | `saveSemanticMemory` |
| `save_sync_memory` | `saveSyncMemory` |
| `save_workflow_memory` | `saveWorkflowMemory` |
| `search_runtime_memory` | `searchRuntimeMemory` |
| `simulate_runtime_execution` | `simulateRuntimeExecution` |
| `stream_extract` | `streamExtract` |
| `universal_extract` | `universalExtract` |
| `validate_reconstructed_runtime` | `validateReconstructedRuntime` |
| `validate_replay_equivalence` | `validateReplayEquivalence` |
| `version` | `version` |
