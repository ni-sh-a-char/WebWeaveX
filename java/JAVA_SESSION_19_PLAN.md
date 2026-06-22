# JAVA_SESSION_19_PLAN

**Phase A — next slice. Mission active: 80 / 128.**

## Selected target: connectors remainder + memory/runtime orchestrators

Per the Phase-A order (connectors remainder → interaction → auth → repository). Phase 1 must
enumerate unproven manifest APIs in `core.connectors` (live remainder) and the deferred
`core.memory` orchestrator (`run_runtime_memory`, `run_memory_for_extraction`, 37-module).

## Plan

1. Phase 0: rebuild reality (fetch, HEAD==origin/java, matrix, validator, clean verify).
2. Phase 1: per-API relative-aware dependency proof **+ runtime import test** for every remaining
   unproven connector/memory-orchestrator manifest API. Classify CLEAN/BLOCKED. Check
   serializability (S14 self-reference lesson — orchestrators may embed cyclic memory).
3. Phase 3–10: port clean APIs → vectors → byte-exact tests → governance → certify → push.

### Expected gain

- **80 → ~83** (connectors remainder; the memory orchestrator may need projection parity or a
  dedicated slice given its 37-module size).

### Queue after this slice (Phase-A order)

interaction (2) → auth (1) → repository (1). → ~85/128. Then Phase B (bs4-decouple ~26) +
Phase C (lxml extraction ~10) — hierarchised in `JAVA_BLOCKER_HIERARCHY_V2.md`.

**Mission not complete — 80 / 128. Continue.**
