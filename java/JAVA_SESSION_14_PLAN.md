# JAVA_SESSION_14_PLAN

**Phase 11 — next family. Mission active: 61 / 128.**

## Selected target: `core.streaming` family (4 APIs)

Per priority order (streaming → reconstruction → memory → identity → auth → repository →
connectors-live → interaction), `core.streaming` is the highest-priority clean cluster.

### Why streaming next (machine-derived)

| Candidate | clean APIs | new substrate | priority rank |
| --- | ---: | --- | ---: |
| **streaming** | **4** | **none (expected)** | **1** |
| reconstruction | 4 | none | 2 |
| memory | 4 | none | 3 |
| identity | 3 | none | 4 |

Top of the stated priority order and a 4-API clean cluster at zero substrate. Same shape as the
execution/sync/workflow/evolution/causality families just proven: `run_*`/`replay_*` pure
transforms; `save_*`/`load_*` reuse the PyJson/PyJsonParse/Kaalka memory substrate; any
`run_*_for_extraction` reuses `ExecutionRuntime.buildUnifiedRuntimeGraph`.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry core.streaming
# expected: clean (0 forbidden); confirm exact module/line counts live
```

### Blocker status

- **None expected.** Clean family; FS confined to any `save/load_*` memory engine. No upstream
  change required. (Phase 1 re-proof is authoritative.)

### Expected parity gain

- **61 → 65** (+4). Remaining after: 63.

### Substrate impact

- **No new substrate expected.** New `io.webweavex.streaming` package (cluster-local helpers
  only).

### Queue after streaming (priority-ordered)

reconstruction (4) → memory (4) → identity (3) → auth (1) → repository (1, path harness) →
connectors-live (3) → interaction (2). ≈ 18 more clean APIs → ~83/128 with **no upstream
change**.

The two Critical blockers (bs4-decouple ~26 APIs; lxml Soup engine ~10 APIs) remain escalated.

**Mission not complete — 61 / 128. Continue.**
