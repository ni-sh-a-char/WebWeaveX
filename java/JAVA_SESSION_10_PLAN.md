# JAVA_SESSION_10_PLAN

**Phase 10 — next family. Mission active: 37 / 128.**

## Selected target: `core.synchronization` family (6 APIs)

`build_runtime_delta`, `run_synchronized_runtime`, `replay_synchronized_runtime`,
`run_sync_for_extraction`, `save_sync_memory`, `load_sync_memory`.

### Why synchronization next (machine-derived)

| Candidate | APIs | new substrate | parity-surface reduction | score* |
| --- | ---: | --- | ---: | ---: |
| **synchronization** | 6 | **none** | high | **highest** |
| workflows | 7 | none | high | high |
| evolution_runtime | 6 | none | high | high |
| causality | 5 | none | high | medium |

*synchronization edges out: 6 APIs at zero substrate, and its `save_*`/`load_*` members exercise
the freshly-built `PyJsonParse` substrate (validating its reuse), while `build_runtime_delta` /
`replay_synchronized_runtime` are pure dict transforms like the execution family just proven.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry core.synchronization
# expected: 25 modules / ~1262 lines / 0 forbidden
```

### Blocker status

- **None.** Clean family; `load_sync_memory` round-trip uses `PyJsonParse` (built S8). No upstream
  change required.

### Expected parity gain

- **37 → 43** (+6). Remaining after: 85.

### Substrate impact

- **No new substrate.** Reuses StableSerialize, Kaalka, PyJson, PyJsonParse, RuntimeGraph,
  PyRepr. May add a small `io.webweavex.synchronization` package (cluster-local helpers only).

### Risk impact

- Negligible (Low-risk clean family). Continues the substrate-free sweep of the ~46 clean APIs.

### Queue after synchronization (risk-ordered)

workflows (7) → evolution_runtime (6) → causality (5) → streaming (4) → reconstruction (4) →
memory (4) → identity (3) → interaction (2) → connectors live_runtime (3) → auth (1) →
repository (1, path harness). ≈ 43 more clean APIs → ~80/128 with **no upstream change**.

The two Critical blockers (bs4-decouple for ~26 semantic APIs; lxml Soup engine for ~10 HTML
APIs) remain escalated per [`JAVA_BLOCKER_HIERARCHY.md`](JAVA_BLOCKER_HIERARCHY.md).

**The mission is not complete. 37 / 128. Continue reducing parity surface.**
