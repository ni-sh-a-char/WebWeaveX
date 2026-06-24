# JAVA_LEDGER_RECONSTRUCTED

**Session-31 forensic reconstruction from repository state only** (PARITY_MANIFEST.json × tools/gen_java_parity_matrix.JAVA_PROVEN × tools/validate_java_manifest.MAPPING × blocker verdict docs). No prior ledger trusted.

| State | Count |
|---|---:|
| CERTIFIED | 108 |
| BLOCKED | 20 |
| PENDING | 0 |
| UNKNOWN | 0 |
| TOTAL | 128 |

| API | Status | Evidence | Test vectors / verdict |
|---|---|---|---|
| `__version__` | CERTIFIED | io.webweavex.WebWeaveX#VERSION | golden_vectors_s28.json#__version__ |
| `analyze` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `authenticate_runtime` | CERTIFIED | io.webweavex.auth.AuthenticationRuntime#authenticateRuntime | golden_vectors_s19.json#authenticate_runtime |
| `build_browser_identity` | CERTIFIED | io.webweavex.identity.IdentityRuntime#buildBrowserIdentity | golden_vectors_s18.json#build_browser_identity |
| `build_interaction_graph` | CERTIFIED | io.webweavex.interaction.InteractionGraph#buildInteractionGraph | golden_vectors_s6.json#build_interaction_graph |
| `build_runtime_delta` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#buildRuntimeDelta | golden_vectors_s10.json#build_runtime_delta |
| `build_runtime_evolution` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#buildRuntimeEvolution | golden_vectors_s12.json#build_runtime_evolution |
| `build_runtime_graph` | CERTIFIED | io.webweavex.graph.RuntimeGraph#buildParityRuntimeGraph | golden_vectors_s2.json#graph |
| `build_runtime_memory` | CERTIFIED | io.webweavex.memory.RuntimeMemory#build | golden_vectors_s3.json#build_runtime_memory |
| `build_runtime_objective` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#buildRuntimeObjective | golden_vectors_s11.json#build_runtime_objective |
| `build_runtime_sandbox` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#buildRuntimeSandbox | golden_vectors_s9.json#build_runtime_sandbox |
| `build_stream_timeline` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#buildStreamTimeline | golden_vectors_s14.json#build_stream_timeline |
| `build_workflow_plan` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#buildWorkflowPlan | golden_vectors_s11.json#build_workflow_plan |
| `capture_dom_mutations` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#captureDomMutations | golden_vectors_s28.json#capture_dom_mutations |
| `capture_websocket_frames` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#captureWebsocketFrames | golden_vectors_s28.json#capture_websocket_frames |
| `clone_runtime_environment` | CERTIFIED | io.webweavex.reconstruction.ReconstructionRuntime#cloneRuntimeEnvironment | golden_vectors_s16.json#clone_runtime_environment |
| `compile_document` | CERTIFIED | io.webweavex.documents.DocumentSemanticIr#compileDocumentIr | golden_vectors_s28.json#compile_document |
| `compile_repository` | BLOCKED | CPython ast CONDITION-B | JAVA_AST_FINAL_VERDICT.md |
| `compile_unified_runtime_ir` | CERTIFIED | io.webweavex.ir.UnifiedRuntimeIr#compile | golden_vectors_s2.json#unified_ir |
| `compute_global_runtime_fingerprint` | CERTIFIED | io.webweavex.determinism.GlobalRuntimeFingerprint#compute | golden_vectors_s2.json#global_fingerprint |
| `compute_kaalka_hash` | CERTIFIED | io.webweavex.crypto.Kaalka#computeKaalkaHash | golden_vectors.json#crypto |
| `crawl` | BLOCKED | network | JAVA_EXTRACTION_BLOCKER_PROOF.md |
| `crawl_async` | BLOCKED | network | JAVA_EXTRACTION_BLOCKER_PROOF.md |
| `decrypt_session_state` | CERTIFIED | io.webweavex.crypto.KaalkaSession#decryptSessionState | golden_vectors_s8.json#decrypt_session_state |
| `decrypt_value` | CERTIFIED | io.webweavex.crypto.Kaalka#decryptValue | golden_vectors.json#crypto |
| `encrypt_session_state` | CERTIFIED | io.webweavex.crypto.KaalkaSession#encryptSessionState | golden_vectors_s8.json#encrypt_session_state |
| `encrypt_value` | CERTIFIED | io.webweavex.crypto.Kaalka#encryptValue | golden_vectors.json#crypto |
| `evolve_selector_runtime` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#evolveSelectorRuntime | golden_vectors_s12.json#evolve_selector_runtime |
| `execute_runtime_action` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#executeRuntimeAction | golden_vectors_s9.json#execute_runtime_action |
| `execute_runtime_objective` | CERTIFIED | io.webweavex.application.ObjectiveExecution#executeRuntimeObjective | golden_vectors_s19.json#execute_runtime_objective |
| `extract` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `extract_api_runtime` | CERTIFIED | io.webweavex.connectors.ApiConnectors#extractApiRuntime | golden_vectors_s4.json#extract_api_runtime |
| `extract_async` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `extract_container_runtime` | CERTIFIED | io.webweavex.connectors.ContainerConnector#extractContainerRuntime | golden_vectors_s7.json#extract_container_runtime |
| `extract_database_runtime` | CERTIFIED | io.webweavex.connectors.DatabaseConnectors#extractDatabaseRuntime | golden_vectors_s4.json#extract_database_runtime |
| `extract_docs` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `extract_document_runtime` | CERTIFIED | io.webweavex.documents.DocumentRuntime#extractDocumentRuntime | golden_vectors_s4b.json#extract_document_runtime |
| `extract_ide_runtime` | CERTIFIED | io.webweavex.connectors.IdeConnector#extractIdeRuntime | golden_vectors_s7.json#extract_ide_runtime |
| `extract_infinite_scroll` | CERTIFIED | io.webweavex.interaction.InfiniteScroll#extractInfiniteScroll | golden_vectors_s28.json#extract_infinite_scroll |
| `extract_kubernetes_runtime` | CERTIFIED | io.webweavex.connectors.KubernetesConnector#extractKubernetesRuntime | golden_vectors_s7.json#extract_kubernetes_runtime |
| `extract_multimodal` | BLOCKED | OCR runtime | JAVA_OCR_VERDICT.md |
| `extract_native` | BLOCKED | OS sys.platform | JAVA_PLATFORM_VERDICT.md |
| `extract_paginated_content` | CERTIFIED | io.webweavex.interaction.Pagination#extractPaginatedContent | golden_vectors_s4b.json#extract_paginated_content |
| `extract_recursive` | BLOCKED | lxml+network | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `extract_repo` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `extract_repository` | BLOCKED | filesystem os.walk | JAVA_PLATFORM_VERDICT.md |
| `extract_runtime_streams` | CERTIFIED | io.webweavex.connectors.StreamConnectors#extractRuntimeStreams | golden_vectors_s4.json#extract_runtime_streams |
| `extract_telemetry_runtime` | CERTIFIED | io.webweavex.connectors.TelemetryConnector#extractTelemetryRuntime | golden_vectors_s4.json#extract_telemetry_runtime |
| `extract_web` | BLOCKED | Playwright live render | JAVA_PLAYWRIGHT_VERDICT.md |
| `fabricate_runtime_reality` | CERTIFIED | io.webweavex.reconstruction.ReconstructionRuntime#fabricateRuntimeReality | golden_vectors_s16.json#fabricate_runtime_reality |
| `fingerprint` | CERTIFIED | io.webweavex.persistence.FingerprintHex#fingerprint | golden_vectors_s2.json#fingerprint |
| `get_runtime_kernel` | CERTIFIED | io.webweavex.kernel.RuntimeKernel#getRuntimeKernel | golden_vectors_s30.json#get_runtime_kernel |
| `heal_selector` | CERTIFIED | io.webweavex.adaptive.SelectorHealing#healSelector | golden_vectors_s21.json#heal_selector |
| `ingest_input` | BLOCKED | OCR (image branch) | JAVA_OCR_VERDICT.md |
| `load_adaptive_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#loadAdaptiveMemory | golden_vectors_s17.json#load_adaptive_memory |
| `load_application_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#loadApplicationMemory | golden_vectors_s17.json#load_application_memory |
| `load_browser_identity` | CERTIFIED | io.webweavex.identity.IdentityRuntime#loadBrowserIdentity | golden_vectors_s18.json#load_browser_identity |
| `load_causal_memory` | CERTIFIED | io.webweavex.causality.CausalityRuntime#loadCausalMemory | golden_vectors_s13.json#load_causal_memory |
| `load_distributed_checkpoint` | CERTIFIED | io.webweavex.distributed.DistributedCheckpoint#loadDistributedCheckpoint | golden_vectors_s19.json#load_distributed_checkpoint |
| `load_encrypted_session` | CERTIFIED | io.webweavex.session.EncryptedSessionStore#loadEncryptedSession | golden_vectors_s8.json#load_encrypted_session |
| `load_evolution_runtime` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#loadEvolutionRuntime | golden_vectors_s12.json#load_evolution_runtime |
| `load_live_runtime` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#loadLiveRuntime | golden_vectors_s14.json#load_live_runtime |
| `load_native_runtime` | CERTIFIED | io.webweavex.memory.NativeRuntimePersistence#loadNativeRuntime | golden_vectors_s19.json#load_native_runtime |
| `load_runtime_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#loadRuntimeMemory | golden_vectors_s17.json#load_runtime_memory |
| `load_semantic_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#loadSemanticMemory | golden_vectors_s17.json#load_semantic_memory |
| `load_sync_memory` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#loadSyncMemory | golden_vectors_s10.json#load_sync_memory |
| `load_workflow_memory` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#loadWorkflowMemory | golden_vectors_s11.json#load_workflow_memory |
| `query_documents` | CERTIFIED | io.webweavex.documents.DocumentSemanticIr#queryDocuments | golden_vectors_s22.json#query_documents |
| `query_graph` | CERTIFIED | io.webweavex.query.GraphQuery#queryGraph | golden_vectors_s3.json#query_graph |
| `query_knowledge` | CERTIFIED | io.webweavex.query.OntologyQuery#queryKnowledge | golden_vectors_s3.json#query_knowledge |
| `query_repo` | CERTIFIED | io.webweavex.repository.RepositoryQuery#queryRepository | golden_vectors_s28.json#query_repo |
| `query_repository` | CERTIFIED | io.webweavex.repository.RepositoryQuery#queryRepository | golden_vectors_s19.json#query_repository |
| `query_runtime_graph` | CERTIFIED | io.webweavex.query.GraphQuery#queryRuntimeGraph | golden_vectors_s3.json#query_runtime_graph |
| `query_runtime_memory` | CERTIFIED | io.webweavex.memory.MemoryQuery#queryRuntimeMemory | golden_vectors_s3.json#query_runtime_memory |
| `query_semantics` | BLOCKED | CPython ast CONDITION-B | JAVA_AST_FINAL_VERDICT.md |
| `reason_semantically` | BLOCKED | CPython ast CONDITION-B | JAVA_AST_FINAL_VERDICT.md |
| `reconstruct_runtime` | CERTIFIED | io.webweavex.reconstruction.RuntimeReconstruction#reconstructRuntime | golden_vectors_s3.json#reconstruct_runtime |
| `recover_modal_runtime` | CERTIFIED | io.webweavex.adaptive.ModalRecovery#recoverModalRuntime | golden_vectors_s15.json#recover_modal_runtime |
| `replay_causal_runtime` | CERTIFIED | io.webweavex.causality.CausalityRuntime#replayCausalRuntime | golden_vectors_s13.json#replay_causal_runtime |
| `replay_interactions` | CERTIFIED | io.webweavex.interaction.InteractionReplay#replayInteractions | golden_vectors_s28.json#replay_interactions |
| `replay_runtime_execution` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#replayRuntimeExecution | golden_vectors_s9.json#replay_runtime_execution |
| `replay_semantic_runtime` | CERTIFIED | io.webweavex.semantic.SemanticReplay#replaySemanticRuntime | golden_vectors_s19.json#replay_semantic_runtime |
| `replay_stream_events` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#replayStreamEvents | golden_vectors_s14.json#replay_stream_events |
| `replay_synchronized_runtime` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#replaySynchronizedRuntime | golden_vectors_s10.json#replay_synchronized_runtime |
| `replay_workflow_runtime` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#replayWorkflowRuntime | golden_vectors_s11.json#replay_workflow_runtime |
| `run_application_cognition` | CERTIFIED | io.webweavex.application.ApplicationCognitionRuntime#runApplicationCognition | golden_vectors_s26.json#run_application_cognition |
| `run_autonomous_extraction` | CERTIFIED | io.webweavex.distributed.AutonomousExtraction#runAutonomousExtraction | golden_vectors_s30.json#run_autonomous_extraction |
| `run_autonomous_workflow` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#runAutonomousWorkflow | golden_vectors_s11.json#run_autonomous_workflow |
| `run_canonical_pipeline` | BLOCKED | aggregator inherits lxml/PW/OCR/fs | JAVA_PENDING_API_AUDIT.md |
| `run_causality_for_extraction` | CERTIFIED | io.webweavex.causality.CausalityRuntime#runCausalityForExtraction | golden_vectors_s13.json#run_causality_for_extraction |
| `run_causality_runtime` | CERTIFIED | io.webweavex.causality.CausalityRuntime#runCausalityRuntime | golden_vectors_s13.json#run_causality_runtime |
| `run_evolution_for_extraction` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#runEvolutionForExtraction | golden_vectors_s12.json#run_evolution_for_extraction |
| `run_evolution_runtime` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#runEvolutionRuntime | golden_vectors_s12.json#run_evolution_runtime |
| `run_execution_for_extraction` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#runExecutionForExtraction | golden_vectors_s9.json#run_execution_for_extraction |
| `run_execution_runtime` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#runExecutionRuntime | golden_vectors_s9.json#run_execution_runtime |
| `run_live_runtime` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#runLiveRuntime | golden_vectors_s14.json#run_live_runtime |
| `run_memory_for_extraction` | CERTIFIED | io.webweavex.memory.RuntimeMemoryRuntime#runMemoryForExtraction | golden_vectors_s20.json#run_memory_for_extraction |
| `run_native_cognition` | BLOCKED | OS sys.platform | JAVA_PLATFORM_VERDICT.md |
| `run_reconstruction_for_extraction` | CERTIFIED | io.webweavex.reconstruction.ReconstructionRuntime#runReconstructionForExtraction | golden_vectors_s16.json#run_reconstruction_for_extraction |
| `run_reconstruction_runtime` | CERTIFIED | io.webweavex.reconstruction.ReconstructionRuntime#runReconstructionRuntime | golden_vectors_s16.json#run_reconstruction_runtime |
| `run_runtime_memory` | CERTIFIED | io.webweavex.memory.RuntimeMemoryRuntime#runRuntimeMemory | golden_vectors_s20.json#run_runtime_memory |
| `run_semantic_for_extraction` | CERTIFIED | io.webweavex.semantic.SemanticRuntime#runSemanticForExtraction | golden_vectors_s25.json#run_semantic_for_extraction |
| `run_semantic_runtime` | CERTIFIED | io.webweavex.semantic.SemanticRuntime#runSemanticRuntime | golden_vectors_s25.json#run_semantic_runtime |
| `run_sync_for_extraction` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#runSyncForExtraction | golden_vectors_s10.json#run_sync_for_extraction |
| `run_synchronized_runtime` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#runSynchronizedRuntime | golden_vectors_s10.json#run_synchronized_runtime |
| `run_workflow_for_extraction` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#runWorkflowForExtraction | golden_vectors_s11.json#run_workflow_for_extraction |
| `RuntimeKernel` | CERTIFIED | io.webweavex.kernel.RuntimeKernel#runPipeline | golden_vectors_s30.json#RuntimeKernel |
| `save_adaptive_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#saveAdaptiveMemory | golden_vectors_s17.json#save_adaptive_memory |
| `save_application_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#saveApplicationMemory | golden_vectors_s17.json#save_application_memory |
| `save_browser_identity` | CERTIFIED | io.webweavex.identity.IdentityRuntime#saveBrowserIdentity | golden_vectors_s18.json#save_browser_identity |
| `save_causal_memory` | CERTIFIED | io.webweavex.causality.CausalityRuntime#saveCausalMemory | golden_vectors_s13.json#save_causal_memory |
| `save_distributed_checkpoint` | CERTIFIED | io.webweavex.distributed.DistributedCheckpoint#saveDistributedCheckpoint | golden_vectors_s19.json#save_distributed_checkpoint |
| `save_encrypted_session` | CERTIFIED | io.webweavex.session.EncryptedSessionStore#saveEncryptedSession | golden_vectors_s8.json#save_encrypted_session |
| `save_evolution_runtime` | CERTIFIED | io.webweavex.evolution.EvolutionRuntime#saveEvolutionRuntime | golden_vectors_s12.json#save_evolution_runtime |
| `save_live_runtime` | CERTIFIED | io.webweavex.streaming.StreamingRuntime#saveLiveRuntime | golden_vectors_s14.json#save_live_runtime |
| `save_native_runtime` | CERTIFIED | io.webweavex.memory.NativeRuntimePersistence#saveNativeRuntime | golden_vectors_s19.json#save_native_runtime |
| `save_runtime_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#saveRuntimeMemory | golden_vectors_s17.json#save_runtime_memory |
| `save_semantic_memory` | CERTIFIED | io.webweavex.memory.MemoryPersistence#saveSemanticMemory | golden_vectors_s17.json#save_semantic_memory |
| `save_sync_memory` | CERTIFIED | io.webweavex.synchronization.SyncRuntime#saveSyncMemory | golden_vectors_s10.json#save_sync_memory |
| `save_workflow_memory` | CERTIFIED | io.webweavex.workflow.WorkflowRuntime#saveWorkflowMemory | golden_vectors_s11.json#save_workflow_memory |
| `search_runtime_memory` | CERTIFIED | io.webweavex.memory.MemorySearch#searchRuntimeMemory | golden_vectors_s3.json#search_runtime_memory |
| `simulate_runtime_execution` | CERTIFIED | io.webweavex.execution.ExecutionRuntime#simulateRuntimeExecution | golden_vectors_s9.json#simulate_runtime_execution |
| `stream_extract` | BLOCKED | lxml CASE-B | JAVA_EXTRACTION_FINAL_VERDICT.md |
| `universal_extract` | BLOCKED | OCR/filesystem | JAVA_OCR_VERDICT.md |
| `UniversalInput` | CERTIFIED | io.webweavex.kernel.UniversalInput | golden_vectors_s2.json#universal_input |
| `validate_reconstructed_runtime` | CERTIFIED | io.webweavex.reconstruction.RuntimeValidation#validateReconstructedRuntime | golden_vectors_s3.json#validate_reconstructed_runtime |
| `validate_replay_equivalence` | CERTIFIED | io.webweavex.replay.ReplayEquivalence#validate | golden_vectors_s2.json#replay |
| `version` | CERTIFIED | io.webweavex.WebWeaveX#VERSION | golden_vectors_s28.json#version |

**Reconstructed totals: 108 CERTIFIED + 20 BLOCKED + 0 PENDING + 0 UNKNOWN = 128.**
Unknowns: none