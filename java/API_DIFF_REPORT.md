# API_DIFF_REPORT

**Session-33 per-API 4-language diff, source-derived. Python canonical (128).**

| API | Languages present | Java | Notes |
|---|---|---|---|
| `__version__` | Py+JS+Dart+Java | ✅ |  |
| `analyze` | Py+JS+Dart | ❌ | lxml |
| `authenticate_runtime` | Py+JS+Dart+Java | ✅ |  |
| `build_browser_identity` | Py+JS+Dart+Java | ✅ |  |
| `build_interaction_graph` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_delta` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_evolution` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_graph` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_objective` | Py+JS+Dart+Java | ✅ |  |
| `build_runtime_sandbox` | Py+JS+Dart+Java | ✅ |  |
| `build_stream_timeline` | Py+JS+Dart+Java | ✅ |  |
| `build_workflow_plan` | Py+JS+Dart+Java | ✅ |  |
| `capture_dom_mutations` | Py+JS+Java | ✅ |  |
| `capture_websocket_frames` | Py+JS+Java | ✅ |  |
| `clone_runtime_environment` | Py+JS+Dart+Java | ✅ |  |
| `compile_document` | Py+JS+Dart+Java | ✅ |  |
| `compile_repository` | Py+JS+Dart | ❌ | repository-semantic-IR + AST |
| `compile_unified_runtime_ir` | Py+JS+Dart+Java | ✅ |  |
| `compute_global_runtime_fingerprint` | Py+JS+Dart+Java | ✅ |  |
| `compute_kaalka_hash` | Py+JS+Dart+Java | ✅ |  |
| `crawl` | Py+JS | ❌ | network requests + regex (regex portable) |
| `crawl_async` | Py+JS | ❌ | network |
| `decrypt_session_state` | Py+JS+Dart+Java | ✅ |  |
| `decrypt_value` | Py+JS+Dart+Java | ✅ |  |
| `encrypt_session_state` | Py+JS+Dart+Java | ✅ |  |
| `encrypt_value` | Py+JS+Dart+Java | ✅ |  |
| `evolve_selector_runtime` | Py+JS+Dart+Java | ✅ |  |
| `execute_runtime_action` | Py+JS+Dart+Java | ✅ |  |
| `execute_runtime_objective` | Py+JS+Dart+Java | ✅ |  |
| `extract` | Py+JS | ❌ | lxml HTML parser |
| `extract_api_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_async` | Py+JS | ❌ | lxml |
| `extract_container_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_database_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_docs` | Py+JS | ❌ | lxml |
| `extract_document_runtime` | Py+JS+Java | ✅ |  |
| `extract_ide_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_infinite_scroll` | Py+JS+Java | ✅ |  |
| `extract_kubernetes_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_multimodal` | Py+JS+Dart+Java | ✅ |  |
| `extract_native` | Py+JS | ❌ | sys.platform + live OS enum |
| `extract_paginated_content` | Py+JS+Dart+Java | ✅ |  |
| `extract_recursive` | Py+JS | ❌ | lxml+network |
| `extract_repo` | Py+JS | ❌ | lxml |
| `extract_repository` | Py+JS | ❌ | filesystem os.walk |
| `extract_runtime_streams` | Py+JS+Dart+Java | ✅ |  |
| `extract_telemetry_runtime` | Py+JS+Dart+Java | ✅ |  |
| `extract_web` | Py+JS | ❌ | Playwright live render |
| `fabricate_runtime_reality` | Py+JS+Dart+Java | ✅ |  |
| `fingerprint` | Py+JS+Dart+Java | ✅ |  |
| `get_runtime_kernel` | Py+JS+Dart+Java | ✅ |  |
| `heal_selector` | Py+JS+Dart+Java | ✅ |  |
| `ingest_input` | Py+JS+Dart+Java | ✅ |  |
| `load_adaptive_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_application_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_browser_identity` | Py+JS+Dart+Java | ✅ |  |
| `load_causal_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_distributed_checkpoint` | Py+JS+Dart+Java | ✅ |  |
| `load_encrypted_session` | Py+JS+Dart+Java | ✅ |  |
| `load_evolution_runtime` | Py+JS+Dart+Java | ✅ |  |
| `load_live_runtime` | Py+JS+Dart+Java | ✅ |  |
| `load_native_runtime` | Py+JS+Dart+Java | ✅ |  |
| `load_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_semantic_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_sync_memory` | Py+JS+Dart+Java | ✅ |  |
| `load_workflow_memory` | Py+JS+Dart+Java | ✅ |  |
| `query_documents` | Py+JS+Dart+Java | ✅ |  |
| `query_graph` | Py+JS+Dart+Java | ✅ |  |
| `query_knowledge` | Py+JS+Dart+Java | ✅ |  |
| `query_repo` | Py+JS+Dart+Java | ✅ |  |
| `query_repository` | Py+JS+Dart+Java | ✅ |  |
| `query_runtime_graph` | Py+JS+Dart+Java | ✅ |  |
| `query_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `query_semantics` | Py+JS+Dart | ❌ | repository-semantic-IR (~3600L epistemic) for repository branch; doc/graph/knowledge branches reuse certified Java engines |
| `reason_semantically` | Py+JS+Dart | ❌ | repository-semantic-IR for runtime branch; discourse/topology branches portable |
| `reconstruct_runtime` | Py+JS+Dart+Java | ✅ |  |
| `recover_modal_runtime` | Py+JS+Dart+Java | ✅ |  |
| `replay_causal_runtime` | Py+JS+Dart+Java | ✅ |  |
| `replay_interactions` | Py+JS+Dart+Java | ✅ |  |
| `replay_runtime_execution` | Py+JS+Dart+Java | ✅ |  |
| `replay_semantic_runtime` | Py+JS+Dart+Java | ✅ |  |
| `replay_stream_events` | Py+JS+Dart+Java | ✅ |  |
| `replay_synchronized_runtime` | Py+JS+Dart+Java | ✅ |  |
| `replay_workflow_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_application_cognition` | Py+JS+Dart+Java | ✅ |  |
| `run_autonomous_extraction` | Py+JS+Java | ✅ |  |
| `run_autonomous_workflow` | Py+JS+Dart+Java | ✅ |  |
| `run_canonical_pipeline` | Py+JS+Dart | ❌ | lxml aggregator |
| `run_causality_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_causality_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_evolution_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_evolution_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_execution_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_execution_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_live_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_memory_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_native_cognition` | Py+JS | ❌ | sys.platform |
| `run_reconstruction_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_reconstruction_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `run_semantic_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_semantic_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_sync_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `run_synchronized_runtime` | Py+JS+Dart+Java | ✅ |  |
| `run_workflow_for_extraction` | Py+JS+Dart+Java | ✅ |  |
| `RuntimeKernel` | Py+JS+Dart+Java | ✅ |  |
| `save_adaptive_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_application_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_browser_identity` | Py+JS+Dart+Java | ✅ |  |
| `save_causal_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_distributed_checkpoint` | Py+JS+Dart+Java | ✅ |  |
| `save_encrypted_session` | Py+JS+Dart+Java | ✅ |  |
| `save_evolution_runtime` | Py+JS+Dart+Java | ✅ |  |
| `save_live_runtime` | Py+JS+Dart+Java | ✅ |  |
| `save_native_runtime` | Py+JS+Dart+Java | ✅ |  |
| `save_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_semantic_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_sync_memory` | Py+JS+Dart+Java | ✅ |  |
| `save_workflow_memory` | Py+JS+Dart+Java | ✅ |  |
| `search_runtime_memory` | Py+JS+Dart+Java | ✅ |  |
| `simulate_runtime_execution` | Py+JS+Dart+Java | ✅ |  |
| `stream_extract` | Py+JS | ❌ | lxml |
| `universal_extract` | Py+JS | ❌ | file extractors + fs repository |
| `UniversalInput` | Py+JS+Dart+Java | ✅ |  |
| `validate_reconstructed_runtime` | Py+JS+Dart+Java | ✅ |  |
| `validate_replay_equivalence` | Py+JS+Dart+Java | ✅ |  |
| `version` | Py+JS+Dart+Java | ✅ |  |