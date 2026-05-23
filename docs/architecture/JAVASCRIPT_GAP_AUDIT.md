# JavaScript Gap Audit (vs Python canonical)

**Reference:** `python` branch · **Audited:** `javascript` @ `origin/javascript`  
**Date:** 2026-05-23

This audit separates **canonical runtime contract** (cross-language lock) from **Python production extensions** (multi-engine packages). Goal: operational equivalence on the contract; honest documentation of Python-only depth.

---

## Summary

| Tier | JavaScript | Notes |
|------|:----------:|-------|
| **Canonical crypto/graph parity** | ✅ | 11/11 vectors; reference implementation |
| **Canonical replay checks** | ✅+ | Matches spec; **exceeds** Python `replay_equivalence_engine.py` (DOM + semantic_fingerprint) |
| **Canonical memory (graph fabric)** | ✅ | `buildRuntimeMemory`, `stableMemoryHash`, `queryRuntimeMemory` |
| **Canonical reconstruction (graph IR)** | ✅ | `reconstructRuntime` on extraction envelope |
| **Python production memory fabric** | ❌ | No semantic/lineage/checkpoint engines |
| **Python production reconstruction** | ❌ | No 19-engine orchestrator |
| **Python production browser stack** | ⚠️ | Playwright + auth file; no interaction/navigation engines |
| **Validation depth** | ⚠️ | Parity + production smoke; no `validation/replay/` tree |

---

## Capability matrix

| Capability | Python | JavaScript | Status |
|------------|--------|------------|--------|
| `normalize_runtime_value` / NFKC | Full (stdlib) | Full (V8) | ✅ |
| `stable_serialize` + volatile keys | Full | Full | ✅ |
| Kaalka v5 `_proc` + base64 | Full | Full | ✅ |
| `compute_deterministic_hash` | Full | Full | ✅ |
| `build_runtime_graph` (parity shape) | Full | Full | ✅ |
| `validate_replay_equivalence` | Core (3 checks) | Full spec (5+ checks) | ✅ |
| DOM stabilization | Full | Full | ✅ |
| `build_runtime_memory` (graph+history) | Parity + extended API | Graph fabric | ✅ contract |
| `query_runtime_memory` | Extended query API | Keyed query | ⚠️ API shape differs |
| `reconstruct_runtime` (envelope) | Extended IR API | Graph extraction | ⚠️ contract subset |
| `extract_web` + auth session | Full Playwright stack | Playwright + Kaalka session | ⚠️ |
| Semantic memory engines | Full (`core/memory/*`) | None | ❌ production |
| Reconstruction orchestrator | Full | Stub | ❌ production |
| `validation/parity/` | Full | Full | ✅ |
| `validation/replay/` | Partial (pytest) | Missing | ❌ → **add** |
| `validation/runtime_graph/` | Implicit | Missing | ❌ → **add** |
| `validation/runtime_memory/` | Implicit | Missing | ❌ → **add** |
| `validation/reconstruction/` | `reconstruction_validation.py` | Missing | ❌ → **add** |
| Ecosystem validation gate | `final_production_master.py` | Missing | ❌ → **add** |
| README (AI agents + depth) | Full | Good, lighter | ⚠️ → **expand** |

---

## Replay engine

**Python** (`core/replay/replay_equivalence_engine.py`): graph_hash, global_fingerprint, browser_identity.

**JavaScript** (`src/replay/replayEquivalence.ts`): same three + optional `dom_stabilized_hash` + `semantic_fingerprint`.

**Gap:** None on canonical contract. Add `validation/replay/` harness for ecosystem parity reporting.

---

## Reconstruction

**Python production:** multi-engine package (`runtime_reconstruction_orchestrator`, fabrication, snapshots).

**JavaScript:** `reconstructRuntime({ extraction })` — deterministic `runtime_id` from graph hash (canonical).

**Gap:** Production orchestration not ported (by design — Python-only). Canonical reconstruction **present**.

---

## Runtime memory

**Python production:** `build_runtime_memory(history, lineage, semantic_relations)` + `memory_id`.

**JavaScript:** `buildRuntimeMemory(graph, history)` + `stableMemoryHash` over `{ graph, history_len }`.

**Gap:** Extended Python memory API not required for cross-language lock. Add replay **memory_hash** check in ecosystem validator when envelope carries `runtime_memory`.

---

## Browser

**Python:** universal web engine, interaction, auth inject, network capture.

**JavaScript:** Playwright render, capture, extractWeb, encrypted session files.

**Gap:** Operational browser depth is Python-led; JS is **agent-grade** (Playwright + stabilization). Document in README; do not fake feature parity.

---

## Required actions (javascript branch)

1. Add `validation/replay/`, `validation/runtime_graph/`, `validation/runtime_memory/`, `validation/reconstruction/`
2. Add `validation/validateEcosystem.ts` + npm script
3. Expand README: AI agent usage, runtime memory, reconstruction, replay equivalence (match Python section list)
4. Export `computeRuntimeFingerprint` alias → `graphFingerprint`
5. Do **not** remove or simplify Python
