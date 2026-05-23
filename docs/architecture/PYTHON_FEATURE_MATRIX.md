# Python Feature Matrix

**Inspected:** `python` branch production tree · **Ports:** `javascript`, `dart`  
**Legend:** ✅ Full · ⚠ Partial · — Not in port (by design)

| Capability | Python Depth | JS Depth | Dart Depth | Gap |
|------------|--------------|----------|------------|-----|
| Canonical pipeline | ✅ Full | ✅ Full | ✅ Full | — |
| Kaalka v5 parity (11 vectors) | ✅ Full | ✅ Full | ✅ Full | — |
| Playwright extraction | ✅ Full | ✅ Full | — HTTP only | Dart: documented |
| SPA stabilization | ✅ Full | ✅ Full | ✅ Full | — |
| DOM stabilization | ✅ Full | ✅ Full | ✅ Full | — |
| Browser identity | ✅ Full orchestrator | ✅ Full module | ✅ Full module | — |
| Runtime session persistence | ✅ Encrypted store | ✅ Kaalka session | ✅ Kaalka session | — |
| Runtime snapshots | ✅ Full | ✅ Full | ✅ HTTP snapshot | — |
| Authenticated continuation | ✅ Playwright restore | ✅ Playwright + cookies | ✅ HTTP + headers | Dart: bounded |
| Replay equivalence engine | ✅ Core | ✅ Full (+ DOM/memory) | ✅ Full (+ DOM/memory) | — |
| Replay graph | ✅ Hash | ✅ `replayGraph` | ✅ `replay_graph` | — |
| Replay memory | ✅ Semantic | ✅ `replayMemory` | ✅ `replay_memory` | — |
| Replay fingerprint | ✅ Global FP | ✅ `replayFingerprint` | ✅ `replay_fingerprint` | — |
| Full runtime replay validation | ✅ | ✅ `validateFullRuntimeReplay` | ✅ `validateFullRuntimeReplay` | — |
| Runtime graph build/normalize | ✅ Full | ✅ Full | ✅ Full | — |
| Graph replay | ✅ Diff/replay | ✅ `runtimeGraphReplay` | ✅ `runtime_graph_replay` | — |
| Graph reconstruction | ✅ Topology | ✅ `runtimeGraphReconstruction` | ✅ `runtime_graph_reconstruction` | — |
| Runtime memory fabric | ✅ Orchestrator | ✅ Graph + lineage | ✅ Graph + lineage | — |
| Memory lineage | ✅ Semantic lineage | ✅ `memoryLineage` | ✅ `memory_lineage` | — |
| Memory persistence | ✅ Encrypted | ✅ `memoryPersistence` | ⚠ Session pattern | — |
| Memory replay | ✅ Semantic replay | ✅ `memoryReplay` | ✅ `memory_replay` | — |
| Reconstruction runtime | ✅ 19-engine | ✅ Full split modules | ✅ Full split modules | Python deeper production |
| Reconstruction browser | ✅ Full | ✅ `reconstructBrowser` | ✅ `reconstruct_browser` | — |
| Reconstruction replay package | ✅ Replay builder | ✅ `reconstructReplay` | ✅ `reconstruct_replay` | — |
| REST connector | ✅ Full | ✅ `restConnector` | — | Dart: N/A |
| Distributed extraction | ✅ Full | — | — | Python-only |
| Semantic VM / journal | ✅ Full | — | — | Python-only |
| Connector fleet (DB/K8s/…) | ✅ Full | — | — | Python-only |
| `validation/parity/` | ✅ | ✅ | ✅ | — |
| `validation/replay/` | ✅ | ✅ | ✅ | — |
| `validation/runtime_graph/` | ✅ | ✅ | ✅ | — |
| `validation/runtime_memory/` | ✅ | ✅ | ✅ | — |
| `validation/reconstruction/` | ✅ | ✅ | ✅ | — |
| `validation/browser/` | ✅ Reports | ✅ `validateBrowser` | ✅ `validate_browser` | — |
| Ecosystem validation gate | ✅ | ✅ | ✅ | — |

---

## Parity tier statement

| Tier | Description |
|------|-------------|
| **Tier A — Canonical contract** | Normalization, serialization, hashes, encrypt, graph, replay, memory, reconstruction — **matched** across Python, JS, Dart |
| **Tier B — Browser operational** | Playwright depth on Python + JS; Dart uses HTTP-bounded continuation with honest documentation |
| **Tier C — Production fleet** | Connectors, distributed extraction, semantic orchestration — **Python only** (not weakened) |

See [FINAL_TRUE_PARITY_REPORT.md](../../FINAL_TRUE_PARITY_REPORT.md) and [ECOSYSTEM_MATRIX.md](./ECOSYSTEM_MATRIX.md).
