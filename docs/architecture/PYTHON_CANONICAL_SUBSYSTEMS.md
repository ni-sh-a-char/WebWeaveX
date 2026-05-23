# Python Canonical Subsystems

**Branch:** `python` · **Role:** Source of truth for production WebWeaveX  
**Version:** 2.0.0 · **Do not simplify this branch for port parity**

This document inventories every **production subsystem** on the Python branch. JavaScript and Dart ports target **operational equivalence** on the canonical contract; Python retains **full multi-engine depth**.

---

## 1. Runtime engine

| Module | Capability |
|--------|------------|
| `core/kernel/runtime_kernel.py` | `RuntimeKernel` — routes all phases through bridges |
| `core/kernel/runtime_pipeline.py` | `run_canonical_pipeline` — UniversalInput → extraction → kernel → graph |
| `core/kernel/runtime_dispatcher.py` | Phase dispatch by name |
| `core/kernel/runtime_scheduler.py` | Ordered phase scheduling |
| `core/kernel/runtime_graph_bridge.py` | Merges IRs → `build_runtime_graph` |
| `core/kernel/runtime_memory_bridge.py` | Memory phase bridge |
| `core/kernel/runtime_replay.py` | Kernel snapshot replay |
| `core/contracts/runtime_contracts.py` | `UniversalInput`, `RuntimePhase`, ingress |
| `core/contracts/extraction_contracts.py` | `ExtractionRequest` / `ExtractionResult` |
| `core/ingestion/universal_ingestion_engine.py` | URL/PDF/repo/image ingestion routing |
| `core/extract/pipeline.py` | Main text/URL extraction |
| `core/orchestration/orchestration_engine.py` | Top-level extraction orchestration |

---

## 2. Browser systems

| Module | Capability |
|--------|------------|
| `core/browser/playwright_runtime.py` | Playwright launch, render, network capture |
| `core/browser/universal_web_extraction_engine.py` | Full `extract_web` pipeline |
| `core/browser/spa_runtime_stabilizer.py` | SPA framework detection, route stabilization |
| `core/browser/dom_stabilization_engine.py` | Volatile DOM stripping, stabilized hash |
| `core/auth/authentication_runtime_engine.py` | Form/cookie/token authentication |
| `core/auth/session_restoration_engine.py` | Restore session into Playwright |
| `core/session/browser_session_snapshot_engine.py` | Capture/restore cookies, storage, headers |
| `core/session/encrypted_session_store.py` | Kaalka-encrypted session persistence |
| `core/identity/browser_identity_orchestrator.py` | Full browser identity profile |
| `core/identity/identity_replay_engine.py` | Replay stored identity |
| `core/interaction/browser_interaction_engine.py` | Clicks, fills, hovers, waits |
| `core/interaction/interaction_replay_engine.py` | Replay interaction sequences |
| `core/network/network_capture_engine.py` | Playwright request listener |

---

## 3. Replay systems

| Module | Capability |
|--------|------------|
| `core/replay/replay_equivalence_engine.py` | `validate_replay_equivalence` — graph + global fingerprint + browser identity |
| `core/interaction/interaction_replay_store.py` | Encrypted interaction replay persistence |
| `core/runtime/semantic_replay_vm.py` | Semantic event journal replay |
| `core/kernel/runtime_replay.py` | Kernel state replay |
| `core/memory/semantic_replay_engine.py` | Semantic checkpoint replay |

---

## 4. Runtime graph systems

| Module | Capability |
|--------|------------|
| `core/runtime_graph/runtime_graph_engine.py` | `build_runtime_graph` — canonical merge |
| `core/runtime_graph/runtime_graph_query_engine.py` | Node/edge queries |
| `core/runtime_graph/runtime_graph_diff_engine.py` | Graph diff |
| `core/contracts/graph_contracts.py` | `RuntimeGraphContract.normalize` |
| `core/determinism/runtime_graph_parity.py` | Cross-language graph parity builder |
| `core/distributed_extraction/distributed_runtime_graph_engine.py` | Distributed graph federation |

---

## 5. Runtime memory

| Module | Capability |
|--------|------------|
| `core/memory/runtime_memory_orchestrator.py` | Full memory phase orchestration |
| `core/memory/runtime_memory_engine.py` | `build_runtime_memory` — deterministic `memory_id` |
| `core/memory/runtime_graph_memory_engine.py` | Entity/relation memory graph |
| `core/memory/runtime_query_engine.py` | Query by semantic/lineage/topology |
| `core/memory/runtime_merge_engine.py` | Federate multiple memories |
| `core/memory/stable_memory_hash.py` | Kaalka-stable memory fingerprint |
| `core/memory/runtime_memory_persistence_engine.py` | Encrypted memory store |
| `core/memory/semantic_memory_engine.py` | `SemanticMemory` bounded store |
| `core/memory/semantic_continuity_engine.py` | Continuity across checkpoints |

---

## 6. Reconstruction

| Module | Capability |
|--------|------------|
| `core/reconstruction/runtime_reconstruction_orchestrator.py` | Full reconstruction phase |
| `core/reconstruction/runtime_reconstruction_engine.py` | Core IR → `runtime_id` |
| `core/reconstruction/browser_reconstruction_engine.py` | Browser tabs, navigation, session |
| `core/reconstruction/session_reconstruction_engine.py` | Authenticated session bundle |
| `core/reconstruction/runtime_memory_reconstruction.py` | Memory layer rebuild |
| `core/reconstruction/runtime_snapshot_engine.py` | Encrypted reconstruction snapshots |
| `core/reconstruction/runtime_validation_engine.py` | Post-reconstruction integrity |

---

## 7. Determinism

| Module | Capability |
|--------|------------|
| `core/determinism/normalization.py` | NFKC, volatile key stripping |
| `core/determinism/global_runtime_fingerprint.py` | Global runtime fingerprint |
| `core/utils/deterministic_serializer.py` | Sorted-key JSON serialization |
| `core/crypto/kaalka_runtime_engine.py` | `encrypt_value` / `decrypt_value` / hashes |

---

## 8. Connectors (production-only depth)

REST, PostgreSQL, MySQL, SQLite, Redis, Kafka, WebSocket, gRPC, GraphQL, filesystem, Docker, Kubernetes, CI/CD, IDE, telemetry — under `core/connectors/`.

---

## 9. Validation

| Path | Capability |
|------|------------|
| `validation/validate_cross_language_parity.py` | 11-vector Kaalka parity |
| `validation/validate_ecosystem.py` | Ecosystem gate (parity + subsystem smoke) |
| `validation/replay/validate_replay.py` | Replay gate |
| `validation/runtime_graph/validate_runtime_graph.py` | Graph gate |
| `validation/runtime_memory/validate_runtime_memory.py` | Memory gate |
| `validation/reconstruction/validate_reconstruction.py` | Reconstruction gate |
| `validation/final_production_master.py` | Master production validation |
| `tests/absolute_final_validation.py` | End-to-end production gate |

---

## Canonical pipeline

```text
UniversalInput
  → run_canonical_pipeline
  → kind-specific extraction (web: universal_web_extraction_engine)
  → RuntimeKernel.run_pipeline (bridges)
  → build_runtime_graph + normalize
  → ExtractionResult + deterministic_hash
```

See [CANONICAL_RUNTIME_SPEC.md](./CANONICAL_RUNTIME_SPEC.md) for cross-language contract details.
