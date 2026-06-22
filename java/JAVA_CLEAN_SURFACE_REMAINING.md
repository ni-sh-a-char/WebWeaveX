# JAVA_CLEAN_SURFACE_REMAINING

**Phase 8 — exhaustion audit (machine-derived, S19).** Live state: **90/128 proven, 38 remaining.**
Every remaining unproven API was traced (relative-aware) **and runtime-imported** in canonical
Python; serializability checked where relevant.

## Genuinely clean + byte-exact-certifiable (no page / no FS / serializable)

| API | module | status |
| --- | --- | --- |
| `run_runtime_memory` | `memory.runtime_memory_orchestrator` | **CLEAN** — 37 mod / 0 forbidden, import OK, output SERIALIZABLE (verified) |
| `run_memory_for_extraction` | `memory.runtime_memory_orchestrator` | **CLEAN** — same orchestrator |

**The clean surface is down to 2 APIs** (the memory orchestrator) — below the ~5 threshold. These
are the final Phase-A slice (S20). After them, **every remaining API is blocked** by an upstream
forbidden dependency, a live Playwright page, the OS platform, or a real filesystem repo.

## Why the rest is NOT clean (0-forbidden but runtime-bound)

| API | reason |
| --- | --- |
| `capture_dom_mutations`, `capture_websocket_frames` | 0 forbidden imports but require a live Playwright `page` (read `page._test_*` hooks) — cross-language **Deferred** |
| `extract_infinite_scroll`, `replay_interactions` | page-coupled browser interaction handlers |
| `extract_repository` | takes a path → walks a real filesystem repo (env-coupled, like the FS-walk branch) |

These are **Tier 4** (see `JAVA_BLOCKER_HIERARCHY_V2.md`): implementable only via a Playwright-page
mock harness or a fixture repo, not byte-exact against a static oracle.

## Conclusion

After the memory orchestrator (S20 → 92/128), the **dependency-clean, page-free, byte-exact
surface is exhausted**. All further progress requires the Phase-B bs4-decouple campaign, the
Phase-C lxml extraction stack, or a Playwright/platform harness — see the hierarchy.
