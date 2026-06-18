# JAVA_SESSION_9_PLAN

**Phase 10 — next highest-value target. The mission remains active (31 / 128).**

## Selected target: `core.execution` cluster (6 APIs)

`build_runtime_sandbox`, `execute_runtime_action`, `replay_runtime_execution`,
`run_execution_runtime`, `run_execution_for_extraction`, `simulate_runtime_execution`.

### Why execution next (not the higher-count workflows)

With the `json.loads` substrate now built, the selection re-weights toward **parity gain at
zero substrate cost**:

| Candidate | parity | new substrate | risk | score* |
| --- | ---: | --- | --- | ---: |
| **execution** | 6 | **none** | Low | **highest** |
| synchronization | 6 | none (json.loads done) | Low | high |
| workflows | 7 | none (json.loads done) | Low | high |
| streaming | 4 | none | Low | medium |

*execution edges ahead: 6 APIs, **zero** new substrate, and `simulate_runtime_execution` /
`execute_runtime_action` are foundational runtime primitives reused by the sync/causality/
evolution clusters that follow.

### Dependency proof (to re-run at session start)

```
python tools/trace_imports_s5_relative.py    # entry core.execution
# expected: 26 modules / ~1472 lines / 0 forbidden  (recompute, do not trust)
```
Relative-aware closure was **0 forbidden** this session. Re-prove before implementing.

### Blocker status

- **None.** `core.execution` is clean; its `load_*`-style members (if any) now have the
  `PyJsonParse` substrate. No upstream change required.

### Expected parity gain

- **31 → 37** (+6) if the full cluster ports cleanly. Remaining after: 91.

### Substrate impact

- **No new substrate.** Reuses Kaalka, StableSerialize, PyJson, PyJsonParse, PyRepr, Connectors-
  style helpers. May add a small `io.webweavex.execution` package with shared envelope helpers
  (cluster-local, not global substrate).

### After execution (queued, risk-ordered — see `JAVA_PARITY_RISK_REGISTER.md`)

1. `core.synchronization` (6) → 2. `core.workflows` (7) → 3. `core.evolution_runtime` (6) →
4. `core.causality` (5) → 5. `core.streaming` (4) → 6. `core.reconstruction` (4) →
7. `core.memory` (4) → 8. `core.identity` (3) → 9. `core.interaction` (2) → 10. `core.auth` (1)
→ 11. `core.repository` (1, path harness).

That sweep is ~48 clean APIs (→ ~79/128) with **no upstream change**. The two Critical risks
(bs4-decoupling for ~26 semantic/memory APIs; the lxml Soup engine for ~10 HTML-extraction
APIs) are escalated separately per the risk register.

**The mission continues. This is a checkpoint, not a completion.**
