# JAVA_SESSION_11_PLAN

**Phase 11 — next family. Mission active: 43 / 128.**

## Selected target: `core.workflows` family (7 APIs)

`build_runtime_objective`, `build_workflow_plan`, `run_autonomous_workflow`,
`replay_workflow_runtime`, `run_workflow_for_extraction`, `save_workflow_memory`,
`load_workflow_memory`.

### Why workflows next (machine-derived)

| Candidate | clean APIs | new substrate | parity-surface reduction |
| --- | ---: | --- | ---: |
| **workflows** | **7** | **none** | **highest** |
| evolution_runtime | 6 | none | high |
| causality | 5 | none | high |
| streaming | 4 | none | medium |

Largest remaining clean cluster at zero substrate. Its `save_*`/`load_*` members reuse the
PyJson/PyJsonParse/Kaalka substrate (validated by S8 sessions + S10 sync memory); its
`run_*`/`build_*`/`replay_*` members are pure dict transforms like the execution/sync families
just proven; `run_workflow_for_extraction` reuses `ExecutionRuntime.buildUnifiedRuntimeGraph`.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry core.workflows
# expected: 23 modules / ~1166 lines / 0 forbidden
```

### Blocker status

- **None.** Clean family; FS confined to `save/load_workflow_memory` (vectorable like
  sync/session memory). No upstream change required.

### Expected parity gain

- **43 → 50** (+7). Remaining after: 78.

### Substrate impact

- **No new substrate.** New `io.webweavex.workflow` package (cluster-local helpers only).

### Risk impact

- Negligible (Low-risk clean family). Continues the substrate-free sweep.

### Queue after workflows (risk-ordered)

evolution_runtime (6) → causality (5) → streaming (4) → reconstruction (4) → memory (4) →
identity (3) → connectors-live (3) → interaction (2) → auth (1) → repository (1, path harness).
≈ 33 more clean APIs → ~78–83/128 with **no upstream change**.

The two Critical blockers (bs4-decouple ~26 APIs; lxml Soup engine ~10 APIs) remain escalated
per [`JAVA_SESSION_10_BLOCKER_AUDIT.md`](JAVA_SESSION_10_BLOCKER_AUDIT.md).

**Mission not complete — 43 / 128. Continue.**
