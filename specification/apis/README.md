# WebWeaveX API Specification

Canonical public API contract. **`specification/` is the sole authority**; both the
Python (`pip`) and JavaScript (`npm`) implementations MUST expose this surface and
conform to it. Neither implementation defines the specification.

_Generated 2026-06-08T11:53:03.791261+00:00 from the certified public surface (128 names). Python names are
snake_case; the JavaScript implementation exposes camelCase equivalents
(see `docs/specs/api_parity_matrix.json`, verified 128/128)._

## Classes (2)

- `RuntimeKernel`
- `UniversalInput`

## Functions (124)

| Python name | Signature | JS name |
|-------------|-----------|---------|
| `analyze` | `(input_data, edges=None)` | `analyze` |
| `authenticate_runtime` | `(page: 'Any', credentials: 'Dict[str, Any]', config: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `authenticateRuntime` |
| `build_browser_identity` | `(profile_id: 'str' = 'default') -> 'Dict[str, Any]'` | `buildBrowserIdentity` |
| `build_interaction_graph` | `(interactions: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `buildInteractionGraph` |
| `build_runtime_delta` | `(previous: 'Optional[Dict[str, Any]]' = None, current: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `buildRuntimeDelta` |
| `build_runtime_evolution` | `(mutations: 'List[Dict[str, Any]]', lineage: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `buildRuntimeEvolution` |
| `build_runtime_graph` | `(runtime_irs: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `buildRuntimeGraph` |
| `build_runtime_memory` | `(runtime_history: 'Optional[List[Dict[str, Any]]]' = None, lineage: 'Optional[List[Dict[str, Any]]]' = None, semantic_relations: 'Optional[List[Dict[str, Any]]]' = None) -> 'Dict[str, Any]'` | `buildRuntimeMemory` |
| `build_runtime_objective` | `(objective: 'str', priority: 'int' = 0) -> 'Dict[str, Any]'` | `buildRuntimeObjective` |
| `build_runtime_sandbox` | `(runtime: 'str' = 'browser', allowed_actions: 'Optional[List[str]]' = None, rollback_enabled: 'bool' = True, max_actions: 'int' = 1000, timeout_ticks: 'int' = 10000, replay_policy: 'str' = 'strict') -> 'Dict[str, Any]'` | `buildRuntimeSandbox` |
| `build_stream_timeline` | `(events: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `buildStreamTimeline` |
| `build_workflow_plan` | `(objective: 'str', semantic_runtime: 'Optional[Dict[str, Any]]' = None, causality: 'Optional[Dict[str, Any]]' = None, application_runtime: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `buildWorkflowPlan` |
| `capture_dom_mutations` | `(page: 'Any') -> 'Dict[str, Any]'` | `captureDomMutations` |
| `capture_websocket_frames` | `(page: 'Any') -> 'Dict[str, Any]'` | `captureWebsocketFrames` |
| `clone_runtime_environment` | `(source: 'Dict[str, Any]', include_graph: 'bool' = True, include_queues: 'bool' = True) -> 'Dict[str, Any]'` | `cloneRuntimeEnvironment` |
| `compile_document` | `(text: str)` | `compileDocument` |
| `compile_repository` | `(source: str, path: str = '', **kwargs)` | `compileRepository` |
| `compile_unified_runtime_ir` | `(registry: 'Optional[Dict[str, Any]]' = None, graph: 'Optional[Dict[str, Any]]' = None, bus: 'Optional[List[Dict[str, Any]]]' = None, phase_results: 'Optional[List[Dict[str, Any]]]' = None, sources: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `compileUnifiedRuntimeIr` |
| `compute_global_runtime_fingerprint` | `(extraction: 'Optional[Dict[str, Any]]' = None, graph: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, sync: 'Optional[Dict[str, Any]]' = None, reconstruction: 'Optional[Dict[str, Any]]' = None, kaalka_seal: 'str' = '') -> 'str'` | `computeGlobalRuntimeFingerprint` |
| `compute_kaalka_hash` | `(value: 'Any') -> 'str'` | `computeKaalkaHash` |
| `crawl` | `(url: str, **kwargs)` | `crawl` |
| `crawl_async` | `(url: str, **kwargs)` | `crawlAsync` |
| `decrypt_session_state` | `(payload: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `decryptSessionState` |
| `decrypt_value` | `(ciphertext: 'str', key: 'str') -> 'dict[str, Any]'` | `decryptValue` |
| `encrypt_session_state` | `(session: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `encryptSessionState` |
| `encrypt_value` | `(value: 'Any', key: 'str') -> 'dict[str, Any]'` | `encryptValue` |
| `evolve_selector_runtime` | `(selectors: 'Optional[Dict[str, str]]' = None, healed: 'Optional[Dict[str, str]]' = None) -> 'Dict[str, Any]'` | `evolveSelectorRuntime` |
| `execute_runtime_action` | `(raw_action: 'Dict[str, Any]', sandbox: 'Optional[Dict[str, Any]]' = None, policy: 'Optional[Dict[str, Any]]' = None, permissions: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0, mutation_count: 'int' = 0, action_count: 'int' = 0) -> 'Dict[str, Any]'` | `executeRuntimeAction` |
| `execute_runtime_objective` | `(objective: 'str', workflow_graph: 'Dict[str, Any]', action_graph: 'Dict[str, Any]', navigation: 'Dict[str, Any]', adaptive_runtime: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `executeRuntimeObjective` |
| `extract` | `(input_data: 'Union[str, Dict[str, Any]]') -> 'Dict[str, Any]'` | `extract` |
| `extract_api_runtime` | `(api_type: 'str' = 'rest', snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractApiRuntime` |
| `extract_async` | `(input_data: 'Union[str, Dict[str, Any]]') -> 'Dict[str, Any]'` | `extractAsync` |
| `extract_container_runtime` | `(runtime: 'str' = 'docker', snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractContainerRuntime` |
| `extract_database_runtime` | `(database_type: 'str' = 'postgresql', snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractDatabaseRuntime` |
| `extract_docs` | `(source: 'Union[str, Dict[str, Any]]') -> 'Dict[str, Any]'` | `extractDocs` |
| `extract_document_runtime` | `(text: 'str', slides: 'Optional[List[Dict[str, Any]]]' = None, workbook: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractDocumentRuntime` |
| `extract_ide_runtime` | `(ide: 'str' = 'vscode', snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractIdeRuntime` |
| `extract_infinite_scroll` | `(page: 'Any') -> 'Dict[str, Any]'` | `extractInfiniteScroll` |
| `extract_kubernetes_runtime` | `(snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractKubernetesRuntime` |
| `extract_multimodal` | `(path: 'str') -> 'Dict[str, Any]'` | `extractMultimodal` |
| `extract_native` | `(runtime: 'str' = 'desktop', application: 'str' = 'discord', application_cognition: 'bool' = True, persistent_runtime: 'bool' = True, runtime_path: 'str' = 'native.enc', runtime_key: 'str' = 'master-key', snapshot: 'Optional[Dict[str, Any]]' = None, interactions: 'Optional[List[Dict[str, Any]]]' = None, adaptive_runtime: 'Optional[Dict[str, Any]]' = None, application_memory: 'Optional[Dict[str, Any]]' = None, merge_runtime_graph: 'bool' = True, causality_runtime: 'bool' = False, causal_memory_path: 'str' = '', causal_memory_key: 'str' = '', semantic_runtime: 'bool' = False, semantic_memory_path: 'str' = '', semantic_memory_key: 'str' = '', autonomous_workflow: 'bool' = False, workflow_memory_path: 'str' = '', workflow_memory_key: 'str' = '', workflow_objective: 'str' = 'capture_notifications', synchronized_runtime: 'bool' = False, sync_memory_path: 'str' = '', sync_memory_key: 'str' = '', sync_tick: 'int' = 0, evolving_runtime: 'bool' = False, evolution_memory_path: 'str' = '', evolution_memory_key: 'str' = '', live_runtime: 'bool' = False, live_memory_path: 'str' = '', live_memory_key: 'str' = '', live_snapshot: 'Optional[Dict[str, Any]]' = None, federated_memory: 'bool' = False, federated_memory_path: 'str' = '', federated_memory_key: 'str' = '', execution_runtime: 'bool' = False, execution_memory_path: 'str' = '', execution_memory_key: 'str' = '', simulate_execution: 'bool' = False, rollback_enabled: 'bool' = True, reconstruction_runtime: 'bool' = False, reconstruction_memory_path: 'str' = '', reconstruction_memory_key: 'str' = '', fabricate_runtime: 'bool' = False, clone_runtime: 'bool' = False) -> 'Dict[str, Any]'` | `extractNative` |
| `extract_paginated_content` | `(page: 'Any', next_selector: 'str') -> 'Dict[str, Any]'` | `extractPaginatedContent` |
| `extract_recursive` | `(url: str, **kwargs)` | `extractRecursive` |
| `extract_repo` | `(source: 'Union[str, Dict[str, Any]]') -> 'Dict[str, Any]'` | `extractRepo` |
| `extract_repository` | `(path: 'str') -> 'Dict[str, Any]'` | `extractRepository` |
| `extract_runtime_streams` | `(stream_types: 'Optional[List[str]]' = None, snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractRuntimeStreams` |
| `extract_telemetry_runtime` | `(backends: 'Optional[list]' = None, snapshot: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `extractTelemetryRuntime` |
| `extract_web` | `(url: 'str', session: 'Optional[Dict[str, Any]]' = None, authenticated: 'bool' = False, session_path: 'str' = '', encryption_key: 'str' = '', interactions: 'Optional[List[Dict[str, Any]]]' = None, infinite_scroll: 'bool' = False, pagination_selector: 'str' = '', interaction_path: 'str' = '', interaction_key: 'str' = '', stream_runtime: 'bool' = False, websocket_capture: 'bool' = False, mutation_capture: 'bool' = False, stream_path: 'str' = '', stream_key: 'str' = '', browser_identity: 'bool' = False, persistent_identity: 'bool' = False, identity_path: 'str' = '', identity_key: 'str' = '', adaptive_runtime: 'bool' = False, persistent_adaptation: 'bool' = False, adaptation_path: 'str' = '', adaptation_key: 'str' = '', selector_healing: 'bool' = False, modal_recovery: 'bool' = False, pagination_recovery: 'bool' = False, distributed_runtime: 'bool' = False, autonomous_runtime: 'bool' = False, checkpoint_path: 'str' = '', checkpoint_key: 'str' = '', application_cognition: 'bool' = False, objective: 'str' = 'extract_dashboard', persistent_application_memory: 'bool' = False, application_memory_path: 'str' = '', application_memory_key: 'str' = '', causality_runtime: 'bool' = False, causal_memory_path: 'str' = '', causal_memory_key: 'str' = '', semantic_runtime: 'bool' = False, semantic_memory_path: 'str' = '', semantic_memory_key: 'str' = '', autonomous_workflow: 'bool' = False, workflow_memory_path: 'str' = '', workflow_memory_key: 'str' = '', synchronized_runtime: 'bool' = False, sync_memory_path: 'str' = '', sync_memory_key: 'str' = '', sync_tick: 'int' = 0, evolving_runtime: 'bool' = False, evolution_memory_path: 'str' = '', evolution_memory_key: 'str' = '', live_runtime: 'bool' = False, live_memory_path: 'str' = '', live_memory_key: 'str' = '', live_snapshot: 'Optional[Dict[str, Any]]' = None, federated_memory: 'bool' = False, federated_memory_path: 'str' = '', federated_memory_key: 'str' = '', execution_runtime: 'bool' = False, execution_memory_path: 'str' = '', execution_memory_key: 'str' = '', simulate_execution: 'bool' = False, rollback_enabled: 'bool' = True, reconstruction_runtime: 'bool' = False, reconstruction_memory_path: 'str' = '', reconstruction_memory_key: 'str' = '', fabricate_runtime: 'bool' = False, clone_runtime: 'bool' = False) -> 'Dict[str, Any]'` | `extractWeb` |
| `fabricate_runtime_reality` | `(runtime: 'Optional[Dict[str, Any]]' = None, environment: 'Optional[Dict[str, Any]]' = None, browser: 'Optional[Dict[str, Any]]' = None, application: 'Optional[Dict[str, Any]]' = None, portable: 'bool' = True) -> 'Dict[str, Any]'` | `fabricateRuntimeReality` |
| `fingerprint` | `(payload: 'Any', token: 'str' = 'webweavex') -> 'str'` | `fingerprint` |
| `get_runtime_kernel` | `(runtime_type: 'str' = 'browser') -> 'RuntimeKernel'` | `getRuntimeKernel` |
| `heal_selector` | `(selector: 'str', dom_nodes: 'List[Dict[str, Any]]', html: 'str' = '') -> 'Dict[str, Any]'` | `healSelector` |
| `ingest_input` | `(path: 'str') -> 'Dict[str, Any]'` | `ingestInput` |
| `load_adaptive_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadAdaptiveMemory` |
| `load_application_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadApplicationMemory` |
| `load_browser_identity` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadBrowserIdentity` |
| `load_causal_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadCausalMemory` |
| `load_distributed_checkpoint` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadDistributedCheckpoint` |
| `load_encrypted_session` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadEncryptedSession` |
| `load_evolution_runtime` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadEvolutionRuntime` |
| `load_live_runtime` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadLiveRuntime` |
| `load_native_runtime` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadNativeRuntime` |
| `load_runtime_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadRuntimeMemory` |
| `load_semantic_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadSemanticMemory` |
| `load_sync_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadSyncMemory` |
| `load_workflow_memory` | `(path: 'str', key: 'str') -> 'Dict[str, Any]'` | `loadWorkflowMemory` |
| `query_documents` | `(result: dict = None, text: str = '')` | `queryDocuments` |
| `query_graph` | `(result: dict = None, node: str = '', graph: dict = None)` | `queryGraph` |
| `query_knowledge` | `(result: dict = None, entities=None, edges=None)` | `queryKnowledge` |
| `query_repo` | `(result: dict)` | `queryRepo` |
| `query_repository` | `(result: dict = None, source: str = '', path: str = '', **kwargs)` | `queryRepository` |
| `query_runtime_graph` | `(graph: 'Dict[str, Any]', query: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `queryRuntimeGraph` |
| `query_runtime_memory` | `(memory: 'Dict[str, Any]', query_type: 'str' = 'semantic', term: 'str' = '') -> 'Dict[str, Any]'` | `queryRuntimeMemory` |
| `query_semantics` | `(query_type: 'str', payload: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `querySemantics` |
| `reason_semantically` | `(domain: 'str', payload: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `reasonSemantically` |
| `reconstruct_runtime` | `(semantic_ir: 'Optional[Dict[str, Any]]' = None, workflow_ir: 'Optional[Dict[str, Any]]' = None, synchronization_ir: 'Optional[Dict[str, Any]]' = None, execution_ir: 'Optional[Dict[str, Any]]' = None, memory_ir: 'Optional[Dict[str, Any]]' = None, runtime_graph: 'Optional[Dict[str, Any]]' = None, runtime_type: 'str' = 'browser', tick: 'int' = 0) -> 'Dict[str, Any]'` | `reconstructRuntime` |
| `recover_modal_runtime` | `(page: 'Any', html: 'str' = '') -> 'Dict[str, Any]'` | `recoverModalRuntime` |
| `replay_causal_runtime` | `(memory: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `replayCausalRuntime` |
| `replay_interactions` | `(page: 'Any', interaction_log: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `replayInteractions` |
| `replay_runtime_execution` | `(actions: 'List[Dict[str, Any]]', transactions: 'Optional[List[Dict[str, Any]]]' = None, mutations: 'Optional[List[Dict[str, Any]]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `replayRuntimeExecution` |
| `replay_semantic_runtime` | `(memory: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `replaySemanticRuntime` |
| `replay_stream_events` | `(page: 'Any', stream_log: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'` | `replayStreamEvents` |
| `replay_synchronized_runtime` | `(memory: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `replaySynchronizedRuntime` |
| `replay_workflow_runtime` | `(memory: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `replayWorkflowRuntime` |
| `run_application_cognition` | `(url: 'str', html: 'str', interactions: 'Optional[List[Dict[str, Any]]]' = None, memory: 'Optional[Dict[str, Any]]' = None, objective: 'str' = 'extract_dashboard', authenticated: 'bool' = False, identity: 'Optional[Dict[str, Any]]' = None, adaptive_runtime: 'Optional[Dict[str, Any]]' = None, route_history: 'Optional[List[Dict[str, Any]]]' = None, modals: 'Optional[List[Dict[str, Any]]]' = None) -> 'Dict[str, Any]'` | `runApplicationCognition` |
| `run_autonomous_extraction` | `(tasks: 'List[Dict[str, Any]]', workers: 'Optional[List[Dict[str, Any]]]' = None, checkpoint_path: 'str' = '', checkpoint_key: 'str' = '', tick: 'int' = 0, objective_execution: 'bool' = False, objective_name: 'str' = 'monitor_metrics', native_extraction: 'bool' = False, native_runtime: 'str' = 'desktop', causal_runtime: 'bool' = False, semantic_runtime: 'bool' = False, autonomous_workflow: 'bool' = False, workflow_federation: 'bool' = False, synchronized_runtime: 'bool' = False, evolving_runtime: 'bool' = False, evolution_memory_path: 'str' = '', evolution_memory_key: 'str' = '', live_runtime: 'bool' = False, live_memory_path: 'str' = '', live_memory_key: 'str' = '', live_snapshot: 'Optional[Dict[str, Any]]' = None, federated_memory: 'bool' = False, federated_memory_path: 'str' = '', federated_memory_key: 'str' = '', execution_runtime: 'bool' = False, execution_memory_path: 'str' = '', execution_memory_key: 'str' = '', simulate_execution: 'bool' = False, rollback_enabled: 'bool' = True, reconstruction_runtime: 'bool' = False, reconstruction_memory_path: 'str' = '', reconstruction_memory_key: 'str' = '', fabricate_runtime: 'bool' = False, clone_runtime: 'bool' = False) -> 'Dict[str, Any]'` | `runAutonomousExtraction` |
| `run_autonomous_workflow` | `(objective: 'str' = 'extract_dashboard', priority: 'int' = 0, semantic_runtime: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, url: 'str' = '', memory: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0, failures: 'Optional[List[str]]' = None) -> 'Dict[str, Any]'` | `runAutonomousWorkflow` |
| `run_canonical_pipeline` | `(inp: 'UniversalInput', *, phases: 'Optional[List[str]]' = None, options: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `runCanonicalPipeline` |
| `run_causality_for_extraction` | `(causality_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', browser_events: 'Optional[List[Dict[str, Any]]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, interactions: 'Optional[List[Dict[str, Any]]]' = None, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runCausalityForExtraction` |
| `run_causality_runtime` | `(browser_events: 'Optional[List[Dict[str, Any]]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, interactions: 'Optional[List[Dict[str, Any]]]' = None) -> 'Dict[str, Any]'` | `runCausalityRuntime` |
| `run_evolution_for_extraction` | `(evolving_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', adaptive_memory: 'Optional[Dict[str, Any]]' = None, workflow_result: 'Optional[Dict[str, Any]]' = None, semantic_result: 'Optional[Dict[str, Any]]' = None, sync_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, failures: 'Optional[List[str]]' = None, tick: 'int' = 0, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runEvolutionForExtraction` |
| `run_evolution_runtime` | `(adaptive_memory: 'Optional[Dict[str, Any]]' = None, workflow_result: 'Optional[Dict[str, Any]]' = None, semantic_result: 'Optional[Dict[str, Any]]' = None, sync_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, failures: 'Optional[List[str]]' = None, memory: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `runEvolutionRuntime` |
| `run_execution_for_extraction` | `(execution_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', sources: 'Optional[Dict[str, Any]]' = None, workers: 'Optional[List[Dict[str, Any]]]' = None, runtime: 'str' = 'browser', tick: 'int' = 0, simulate_execution: 'bool' = False, rollback_enabled: 'bool' = True, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runExecutionForExtraction` |
| `run_execution_runtime` | `(sources: 'Optional[Dict[str, Any]]' = None, stored: 'Optional[Dict[str, Any]]' = None, workers: 'Optional[List[Dict[str, Any]]]' = None, runtime: 'str' = 'browser', tick: 'int' = 0, simulate: 'bool' = False, rollback_enabled: 'bool' = True) -> 'Dict[str, Any]'` | `runExecutionRuntime` |
| `run_live_runtime` | `(config: 'Optional[Dict[str, Any]]' = None, snapshot: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `runLiveRuntime` |
| `run_memory_for_extraction` | `(federated_memory: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', sources: 'Optional[Dict[str, Any]]' = None, nodes: 'Optional[List[Dict[str, Any]]]' = None, tick: 'int' = 0, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runMemoryForExtraction` |
| `run_native_cognition` | `(runtime: 'str' = 'desktop', application: 'str' = '', snapshot: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, interactions: 'Optional[List[Dict[str, Any]]]' = None, application_cognition: 'bool' = False, adaptive_runtime: 'Optional[Dict[str, Any]]' = None, application_memory: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `runNativeCognition` |
| `run_reconstruction_for_extraction` | `(reconstruction_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', sources: 'Optional[Dict[str, Any]]' = None, runtime_graph: 'Optional[Dict[str, Any]]' = None, runtime_type: 'str' = 'browser', tick: 'int' = 0, fabricate_runtime: 'bool' = False, clone_runtime: 'bool' = False, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runReconstructionForExtraction` |
| `run_reconstruction_runtime` | `(sources: 'Optional[Dict[str, Any]]' = None, stored: 'Optional[Dict[str, Any]]' = None, runtime_graph: 'Optional[Dict[str, Any]]' = None, runtime_type: 'str' = 'browser', tick: 'int' = 0, fabricate: 'bool' = False, clone: 'bool' = False) -> 'Dict[str, Any]'` | `runReconstructionRuntime` |
| `run_runtime_memory` | `(sources: 'Optional[Dict[str, Any]]' = None, stored: 'Optional[Dict[str, Any]]' = None, nodes: 'Optional[List[Dict[str, Any]]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `runRuntimeMemory` |
| `run_semantic_for_extraction` | `(semantic_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', url: 'str' = '', html: 'str' = '', interactions: 'Optional[List[Dict[str, Any]]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, runtime_graph: 'Optional[Dict[str, Any]]' = None, objective: 'str' = '', merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runSemanticForExtraction` |
| `run_semantic_runtime` | `(url: 'str' = '', html: 'str' = '', text: 'str' = '', interactions: 'Optional[List[Dict[str, Any]]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, repository_files: 'Optional[List[str]]' = None, runtime_graph: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, objective: 'str' = '') -> 'Dict[str, Any]'` | `runSemanticRuntime` |
| `run_sync_for_extraction` | `(synchronized_runtime: 'bool' = True, memory_path: 'str' = '', memory_key: 'str' = '', tick: 'int' = 0, browser: 'Optional[Dict[str, Any]]' = None, native: 'Optional[Dict[str, Any]]' = None, semantic_result: 'Optional[Dict[str, Any]]' = None, workflow_result: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, session: 'Optional[Dict[str, Any]]' = None, identity: 'Optional[Dict[str, Any]]' = None, merge_graph: 'bool' = True) -> 'Dict[str, Any]'` | `runSyncForExtraction` |
| `run_synchronized_runtime` | `(tick: 'int' = 0, browser: 'Optional[Dict[str, Any]]' = None, native: 'Optional[Dict[str, Any]]' = None, semantic_result: 'Optional[Dict[str, Any]]' = None, workflow_result: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, session: 'Optional[Dict[str, Any]]' = None, identity: 'Optional[Dict[str, Any]]' = None, memory: 'Optional[Dict[str, Any]]' = None, workers: 'Optional[List[Dict[str, Any]]]' = None) -> 'Dict[str, Any]'` | `runSynchronizedRuntime` |
| `run_workflow_for_extraction` | `(autonomous_workflow: 'bool' = True, objective: 'str' = 'extract_dashboard', memory_path: 'str' = '', memory_key: 'str' = '', url: 'str' = '', semantic_runtime: 'Optional[Dict[str, Any]]' = None, causality_result: 'Optional[Dict[str, Any]]' = None, application_result: 'Optional[Dict[str, Any]]' = None, distributed_result: 'Optional[Dict[str, Any]]' = None, native_cognition: 'Optional[Dict[str, Any]]' = None, merge_graph: 'bool' = True, tick: 'int' = 0) -> 'Dict[str, Any]'` | `runWorkflowForExtraction` |
| `save_adaptive_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveAdaptiveMemory` |
| `save_application_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveApplicationMemory` |
| `save_browser_identity` | `(path: 'str', identity: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveBrowserIdentity` |
| `save_causal_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveCausalMemory` |
| `save_distributed_checkpoint` | `(path: 'str', checkpoint: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveDistributedCheckpoint` |
| `save_encrypted_session` | `(path: 'str', session: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveEncryptedSession` |
| `save_evolution_runtime` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveEvolutionRuntime` |
| `save_live_runtime` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveLiveRuntime` |
| `save_native_runtime` | `(path: 'str', runtime: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveNativeRuntime` |
| `save_runtime_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveRuntimeMemory` |
| `save_semantic_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveSemanticMemory` |
| `save_sync_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveSyncMemory` |
| `save_workflow_memory` | `(path: 'str', memory: 'Dict[str, Any]', key: 'str') -> 'Dict[str, Any]'` | `saveWorkflowMemory` |
| `search_runtime_memory` | `(index: 'Dict[str, Any]', term: 'str', search_type: 'str' = 'structural') -> 'Dict[str, Any]'` | `searchRuntimeMemory` |
| `simulate_runtime_execution` | `(actions: 'List[Dict[str, Any]]', sandbox: 'Optional[Dict[str, Any]]' = None, tick: 'int' = 0) -> 'Dict[str, Any]'` | `simulateRuntimeExecution` |
| `stream_extract` | `(input_data)` | `streamExtract` |
| `universal_extract` | `(path: 'str') -> 'Dict[str, Any]'` | `universalExtract` |
| `validate_reconstructed_runtime` | `(runtime: 'Optional[Dict[str, Any]]' = None, replay: 'Optional[Dict[str, Any]]' = None, topology: 'Optional[Dict[str, Any]]' = None, execution: 'Optional[Dict[str, Any]]' = None, mutations: 'Optional[Dict[str, Any]]' = None) -> 'Dict[str, Any]'` | `validateReconstructedRuntime` |
| `validate_replay_equivalence` | `(original: 'Dict[str, Any]', replayed: 'Dict[str, Any]') -> 'Dict[str, Any]'` | `validateReplayEquivalence` |

## Values (2)

- `__version__` (str)
- `version` (str)

## Conformance
- Every name above MUST be importable and callable in both implementations.
- Pure functions MUST be deterministic and produce specification-equivalent output
  (verified by `validation/equivalence/` against `specification/vectors`).
- See `docs/specs/public_api_execution_report.json` for executed-call evidence.
