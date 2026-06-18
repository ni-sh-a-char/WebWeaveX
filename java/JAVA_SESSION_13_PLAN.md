# JAVA_SESSION_13_PLAN

**Phase 11 — next family. Mission active: 56 / 128.**

## Selected target: `core.causality` family (5 APIs)

`run_causality_runtime`, `replay_causal_runtime`, `run_causality_for_extraction`,
`save_causal_memory`, `load_causal_memory`.

### Why causality next (machine-derived)

| Candidate | clean APIs | new substrate | parity-surface reduction |
| --- | ---: | --- | ---: |
| **causality** | **5** | **none** | **highest** |
| streaming | 4 | none | medium |
| reconstruction | 4 | none | medium |
| memory | 4 | none | medium |

Largest remaining clean cluster at zero substrate. Same shape as execution/sync/workflow/
evolution: `run_*`/`replay_*` pure transforms; `save_*`/`load_*` reuse the PyJson/PyJsonParse/
Kaalka memory substrate; `run_causality_for_extraction` reuses
`ExecutionRuntime.buildUnifiedRuntimeGraph`.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry core.causality
# expected: ~25 modules / ~1360 lines / 0 forbidden
```

### Blocker status

- **None expected.** Clean family; FS confined to `save/load_causal_memory`. No upstream change.

### Expected parity gain

- **56 → 61** (+5). Remaining after: 67.

### Substrate impact

- **No new substrate.** New `io.webweavex.causality` package (cluster-local helpers only).

### Queue after causality (risk-ordered)

streaming (4) → reconstruction (4) → memory (4) → identity (3) → connectors-live (3) →
interaction (2) → auth (1) → repository (1, path harness). ≈ 22 more clean APIs → ~83/128 with
**no upstream change**.

The two Critical blockers (bs4-decouple ~26 APIs; lxml Soup engine ~10 APIs) remain escalated.

**Mission not complete — 56 / 128. Continue.**
