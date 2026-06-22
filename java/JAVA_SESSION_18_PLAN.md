# JAVA_SESSION_18_PLAN

**Phase A — next family. Mission active: 77 / 128.**

## Selected target: `core.identity` family (~3 APIs)

Per the Phase-A order (identity → connectors-live remainder → interaction → auth → repository).

## Plan

1. Phase 0: rebuild reality (fetch, HEAD==origin/java, matrix, validator).
2. Phase 1: enumerate unproven `core.identity` manifest APIs; per-API relative-aware dependency
   proof **plus a runtime import test** (the S17 lesson: trace can miss eager-`__init__` bs4).
   Classify CLEAN/BLOCKED. Check serializability (S14 self-reference lesson).
3. Phase 3–10: port clean APIs → vectors → byte-exact tests → governance → certify → push.

### Expected gain

- **77 → ~80**.

### Substrate impact

- **No new substrate expected.** Reuse determinism/crypto/json.

### Queue after identity (Phase-A order)

connectors-live remainder (run_runtime_memory orchestrator + any live remainder) → interaction (2)
→ auth (1) → repository (1) → plus the deferred `core.memory` orchestrator
(`run_runtime_memory` / `run_memory_for_extraction`, 37-module). → ~83/128.

Then Phase B (bs4-decouple ~26) + Phase C (lxml extraction ~10) — to be hierarchised in
`JAVA_BLOCKER_HIERARCHY_V2.md` once the clean sweep is exhausted.

**Mission not complete — 77 / 128. Continue.**
