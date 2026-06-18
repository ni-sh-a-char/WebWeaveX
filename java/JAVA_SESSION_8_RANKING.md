# JAVA_SESSION_8_RANKING

**Machine-derived ranking, recomputed this session** from repository state
(`tools/rank_remaining_apis.py` over `origin/python` @ `9625f4a`; result
`tools/rank_remaining_apis.result.json`). Not trusted from prior sessions.

## Recomputed totals (pre-slice)

| Class | Count |
| --- | ---: |
| Remaining (rank-tool baseline: 24 proven + 3 special excluded) | 101 |
| Clean-portable (0 forbidden) | 59 |
| Forbidden-blocked | 42 |

> Note: `tools/rank_remaining_apis.py`'s `PROVEN` constant lists the 24 pre-S7 APIs, so its
> raw "59 clean" still counts the 3 Session-7 connectors (now proven) and the 4 Session-8
> session-crypto APIs. **True current state after this slice: 31 proven / 97 remaining**
> (clean-remaining ≈ 52). Cluster *closures* are independent of the proven set, so the cluster
> table below is accurate. Identical to the Session-7 recomputation → ranking is stable.

## Clean clusters (shared closure)

| Cluster | Clean APIs | Closure | New substrate |
| --- | ---: | --- | --- |
| `core.workflows` | 7 | 23 m / 1166 L | json.loads (for `load_workflow_memory`) |
| `core.execution` | 6 | 26 m / 1472 L | none |
| `core.synchronization` | 6 | 25 m / 1262 L | json.loads (load_sync_memory) |
| `core.evolution_runtime` | 6 | 25 m / 1237 L | json.loads (load_evolution_runtime) |
| `core.causality` | 5 | 25 m / 1360 L | json.loads (load_causal_memory) |
| `core.streaming` | 4 | 18 m / 958 L | none |
| `core.reconstruction` | 4 | 24 m / 1407 L | none |
| `core.memory` | 4 | 37 m / 1634 L | json.loads |
| `core.identity` | 3 | 28 m / 1092 L | json.loads (load_browser_identity) |
| **`core.crypto`+`core.session` (session crypto)** | **4** | 4–5 m / 282–362 L | **json.loads (BUILT THIS SLICE)** |
| `core.interaction` | 2 | 19 m / 1174 L | none |
| `core.auth` | 1 | 7 m / 594 L | none |
| `core.repository` | 1 | 12 m / 674 L | path-canonicalization harness |

## Selection score (Phase 1 — machine-derived)

Score = **(parity_gain × reuse_value × blocker_reduction) ÷ new_substrate_cost**, where
`reuse_value` and `blocker_reduction` are the count of *other* remaining APIs unblocked by the
substrate this cluster forces.

| Cluster | parity | reuse | blocker_red | substrate_cost | **score** |
| --- | ---: | ---: | ---: | ---: | ---: |
| **session crypto** | 4 | 10 | 8 | 3 | **106.7** |
| execution | 6 | 2 | 1 | 1 | 12.0 |
| workflows | 7 | 2 | 1 | 2 | 7.0 |
| synchronization | 6 | 2 | 1 | 2 | 6.0 |

`reuse`/`blocker_red` for **session crypto** are high because it forces the JDK-only
`json.loads` substrate (`PyJsonParse`), which every `decrypt_*`/`load_*` roundtrip API across
**≥10 other clusters** depends on (≈30 APIs: `load_workflow_memory`, `load_sync_memory`,
`load_causal_memory`, `load_evolution_runtime`, `load_runtime_memory`, `load_browser_identity`,
`load_live_runtime`, `load_encrypted_session`, …). Per the mission's PRIMARY RULE (eliminate
future blockers, not chase counts), **session crypto wins decisively** despite the lowest raw
parity gain.

## Decision

**Selected cluster: session crypto** (`encrypt_session_state`, `decrypt_session_state`,
`save_encrypted_session`, `load_encrypted_session`) + the `PyJsonParse` `json.loads` substrate.
Implemented in full this slice (**27 → 31 proven**, +4 APIs; the `json.loads` substrate is the
strategic win — it unblocks the `load_*`/`decrypt_*` members of clusters 1–9).
