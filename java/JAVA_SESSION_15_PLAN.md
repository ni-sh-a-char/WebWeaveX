# JAVA_SESSION_15_PLAN

**Phase 11 — next family. Mission active: 66 / 128.**

## Selected target: `core.reconstruction` family (~4 APIs)

Per the Tier-1 clean-sweep priority order (reconstruction → memory → identity → auth →
repository → connectors-live → interaction), `core.reconstruction` is next.

### Why reconstruction next

Highest-priority remaining clean cluster. Note: several reconstruction primitives
(`RuntimeReconstruction`, `RuntimeValidation`, `MemoryReconstruction`, `BrowserReconstruction`)
already exist in `io.webweavex.reconstruction` from the foundation slices — Phase 1 must
distinguish the remaining *manifest-API* reconstruction functions from already-proven ones and
target only the unproven, dependency-clean set.

### Closure proof (re-run at session start — do not trust)

```
python tools/trace_imports_s5_relative.py    # entry the reconstruction API modules
# expected: clean (0 forbidden); confirm exact counts live; watch for the self-reference /
# non-serializable pattern seen in run_live_runtime
```

### Expected parity gain

- **66 → ~70** (depends on how many reconstruction manifest APIs are unproven + clean).

### Substrate impact

- **No new substrate expected.** Reuse determinism/crypto/json + existing reconstruction classes.

### Queue after reconstruction (priority order)

memory (4) → identity (3) → connectors-other (3) → interaction (2) → auth (1) →
repository (1). ≈ 14 more clean APIs → ~84/128 with no upstream change. Then Tier 2
(bs4-decouple ~26) and Tier 3 (lxml extraction ~10) require upstream-canon changes.

**Mission not complete — 66 / 128. Continue.**
