# UNIFIED_PARITY_MATRIX

**Session-31 cross-language convergence matrix — source-derived (PARITY_MANIFEST.json verified against branch exports; Java column from tools/gen_java_parity_matrix.JAVA_PROVEN). Python is canonical.**

| Lang | Surface |
|---|---|
| Python | 128/128 (canonical `__all__`) |
| JavaScript | 128/128 (S31: +version/__version__) |
| Dart | 110/128 |
| Java | 108/128 (20 formally blocked) |

| API | Py | JS | Dart | Java | Status | Notes |
|-----|----|----|------|------|--------|-------|
| `__version__` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `analyze` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml |
| `authenticate_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_browser_identity` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_interaction_graph` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_delta` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_evolution` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_graph` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_objective` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_runtime_sandbox` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_stream_timeline` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `build_workflow_plan` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `capture_dom_mutations` | ✅ | ✅ | ❌ | ✅ | PARTIAL/BLOCKED | Dart Deferred |
| `capture_websocket_frames` | ✅ | ✅ | ❌ | ✅ | PARTIAL/BLOCKED | Dart Deferred |
| `clone_runtime_environment` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `compile_document` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `compile_repository` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: AST |
| `compile_unified_runtime_ir` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `compute_global_runtime_fingerprint` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `compute_kaalka_hash` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `crawl` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: network; Dart Partial |
| `crawl_async` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: network; Dart Partial |
| `decrypt_session_state` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `decrypt_value` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `encrypt_session_state` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `encrypt_value` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `evolve_selector_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `execute_runtime_action` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `execute_runtime_objective` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `extract_api_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_async` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `extract_container_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_database_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_docs` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `extract_document_runtime` | ✅ | ✅ | ❌ | ✅ | PARTIAL/BLOCKED | Dart Partial |
| `extract_ide_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_infinite_scroll` | ✅ | ✅ | ❌ | ✅ | PARTIAL/BLOCKED | Dart Deferred |
| `extract_kubernetes_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_multimodal` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: OCR |
| `extract_native` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: platform; Dart Deferred |
| `extract_paginated_content` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_recursive` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `extract_repo` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `extract_repository` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: fs; Dart Partial |
| `extract_runtime_streams` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_telemetry_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `extract_web` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: playwright; Dart Partial |
| `fabricate_runtime_reality` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `fingerprint` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `get_runtime_kernel` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `heal_selector` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `ingest_input` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: OCR |
| `load_adaptive_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_application_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_browser_identity` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_causal_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_distributed_checkpoint` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_encrypted_session` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_evolution_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_live_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_native_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_semantic_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_sync_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `load_workflow_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_documents` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_graph` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_knowledge` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_repo` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_repository` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_runtime_graph` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `query_semantics` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: AST |
| `reason_semantically` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: AST |
| `reconstruct_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `recover_modal_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_causal_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_interactions` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_runtime_execution` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_semantic_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_stream_events` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_synchronized_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `replay_workflow_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_application_cognition` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_autonomous_extraction` | ✅ | ✅ | ❌ | ✅ | PARTIAL/BLOCKED | Dart Partial |
| `run_autonomous_workflow` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_canonical_pipeline` | ✅ | ✅ | ✅ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml(aggregator) |
| `run_causality_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_causality_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_evolution_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_evolution_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_execution_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_execution_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_live_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_memory_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_native_cognition` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: platform; Dart Deferred |
| `run_reconstruction_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_reconstruction_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_semantic_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_semantic_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_sync_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_synchronized_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `run_workflow_for_extraction` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `RuntimeKernel` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_adaptive_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_application_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_browser_identity` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_causal_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_distributed_checkpoint` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_encrypted_session` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_evolution_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_live_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_native_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_semantic_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_sync_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `save_workflow_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `search_runtime_memory` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `simulate_runtime_execution` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `stream_extract` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: lxml; Dart Partial |
| `universal_extract` | ✅ | ✅ | ❌ | ❌ | PARTIAL/BLOCKED | Java blocked: OCR/fs; Dart Partial |
| `UniversalInput` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `validate_reconstructed_runtime` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `validate_replay_equivalence` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |
| `version` | ✅ | ✅ | ✅ | ✅ | FULL PARITY |  |

**4-way FULL PARITY: 103 / 128.** Remaining 25 have a divergence (Java blocked and/or Dart Partial/Deferred).