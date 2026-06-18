# JAVA_SESSION_8_CLUSTER_ANALYSIS

**Phase 0 — relative-aware closure for every candidate cluster (recomputed this session).**
Tracer: `tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

| Candidate | Entry module | Closure | Forbidden | Shared substrate | Reusable infra | Parity value | Blocker-reduction value |
| --- | --- | --- | :---: | --- | --- | ---: | ---: |
| **session crypto** | `core.crypto.kaalka_session_engine` (+ `core.session.encrypted_session_store`) | 4–5 m / 282–362 L | **0** | **json.loads (PyJsonParse) — NEW** + Kaalka + PyJson (proven) | `PyJsonParse` reused by ~30 `load_*`/`decrypt_*` APIs | 4 | **HIGH (~30)** |
| workflows | `core.workflows` | 23 m / 1166 L | 0 | json.loads (for `load_workflow_memory`) + runtime-graph (proven) | workflow IR helpers (cluster-local) | 7 | low (1) |
| execution | `core.execution` | 26 m / 1472 L | 0 | none new | execution envelope helpers | 6 | none |
| synchronization | `core.synchronization` | 25 m / 1262 L | 0 | json.loads (load_sync_memory) | sync helpers | 6 | low |
| runtime cloning | `core.reconstruction.runtime_clone_engine` | 1 m / 26 L | 0 | none new | trivial | 1 | none |
| modal recovery | `core.adaptive.modal_recovery_engine` | 1 m / 57 L | 0 | none new | trivial | 1 | none |

## Observations

- **All six candidates are forbidden-free** (clean) — selection is about substrate leverage,
  not blocker avoidance.
- **`session crypto` is the only candidate that forces a broadly-reusable substrate**
  (`json.loads`). The `runtime_clone`/`modal_recovery` candidates are 1-module trivial wins
  (good fast follow-ups) but build nothing reusable.
- `workflows`/`execution`/`synchronization` are large multi-API clusters with high parity count
  but mostly cluster-local helpers; several of their `load_*`/`save_*` members were themselves
  blocked on the missing `json.loads` substrate — now unblocked by this slice.

## Selection (see `JAVA_SESSION_8_RANKING.md` for the numeric score)

**session crypto** — maximizes (parity × reuse × blocker_reduction)/substrate_cost = **106.7**,
far above the next candidate (execution, 12.0). The `json.loads` substrate built here is the
highest-leverage infrastructure available among all remaining clusters.
