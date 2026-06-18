# JAVA_SESSION_12_PLAN

**Phase 11 — next family. Mission active: 50 / 128.**

## Selected target: `core.evolution_runtime` family (6 APIs)

`build_runtime_evolution`, `evolve_selector_runtime`, `run_evolution_runtime`,
`run_evolution_for_extraction`, `save_evolution_runtime`, `load_evolution_runtime`.

### Why evolution next (machine-derived)

| Candidate | clean APIs | new substrate | parity-surface reduction |
| --- | ---: | --- | ---: |
| **evolution_runtime** | **6** | **none** | **highest** |
| causality | 5 | none | high |
| streaming | 4 | none | medium |
| reconstruction | 4 | none | medium |

Largest remaining clean cluster at zero substrate. Same shape as the execution/sync/workflow
families just proven: `run_*`/`build_*`/`replay_*` pure transforms; `save_*`/`load_*` reuse the
PyJson/PyJsonParse/Kaalka memory substrate; `run_evolution_for_extraction` reuses
`ExecutionRuntime.buildUnifiedRuntimeGraph`.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry core.evolution_runtime
# expected: ~25 modules / ~1237 lines / 0 forbidden
```

### Blocker status

- **None expected.** Clean family; FS confined to `save/load_evolution_runtime`. No upstream
  change required.

### Expected parity gain

- **50 → 56** (+6). Remaining after: 72.

### Substrate impact

- **No new substrate.** New `io.webweavex.evolution` package (cluster-local helpers only).

### Queue after evolution (risk-ordered)

causality (5) → streaming (4) → reconstruction (4) → memory (4) → identity (3) →
connectors-live (3) → interaction (2) → auth (1) → repository (1, path harness). ≈ 27 more clean
APIs → ~83/128 with **no upstream change**.

The two Critical blockers (bs4-decouple ~26 APIs; lxml Soup engine ~10 APIs) remain escalated
per [`JAVA_SESSION_11_BLOCKER_AUDIT.md`](JAVA_SESSION_11_BLOCKER_AUDIT.md).

**Mission not complete — 50 / 128. Continue.**
