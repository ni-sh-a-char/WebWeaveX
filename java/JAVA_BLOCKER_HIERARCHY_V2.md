# JAVA_BLOCKER_HIERARCHY_V2

**Phase 9 — recomputed blocker hierarchy (machine-derived, S19).** 90/128 proven, 38 remaining.
Every remaining API traced (relative-aware) + runtime-imported in canonical Python. Ranked by
APIs-unlocked ÷ effort. **No bs4/lxml work begun — this is preparation only.**

## Tier 1 — Clean (certifiable now)

| count | APIs |
| ---: | --- |
| **2** | `run_runtime_memory`, `run_memory_for_extraction` (memory orchestrator, 37 mod / 0 forbidden / serializable) |

→ S20 closes these (Phase A complete at ~92/128).

## Tier 2 — bs4-coupled (eager `core.semantic`/`core.evidence` `__init__` or semantic pipeline)

| count | APIs |
| ---: | --- |
| **~9** | `query_documents`, `query_semantics`, `reason_semantically`, `run_semantic_runtime`, `run_semantic_for_extraction`, `extract_multimodal`, `ingest_input`, `heal_selector`, `run_application_cognition` |

**Highest leverage.** A single upstream change — lazy-import BeautifulSoup inside
`core.semantic`/`core.evidence` `__init__` — unblocks this tier **and** the bs4-pulling subset of
Tier 5, with no behavior change. → `JAVA_BS4_DECOUPLE_PLAN.md` (Phase B).

## Tier 3 — lxml / HTML-extraction pipeline (`core.extract.pipeline`, forbidden≈13)

| count | APIs |
| ---: | --- |
| **~6** | `extract`, `extract_docs`, `extract_repo`, `stream_extract`, `extract_web`, `crawl` |

Requires a deterministic lxml/BeautifulSoup-parity Soup engine (the certified Dart approach).
→ `JAVA_LXML_EXTRACTION_PLAN.md` (Phase C).

## Tier 4 — Playwright/platform/FS-coupled (0–6 forbidden, runtime-bound)

| count | APIs |
| ---: | --- |
| **~7** | `capture_dom_mutations`, `capture_websocket_frames`, `extract_infinite_scroll`, `replay_interactions` (page); `extract_native`, `run_native_cognition` (sys.platform); `extract_repository` (FS repo) |

Needs a Playwright-page mock / OS / fixture-repo harness. Permanent-deferred in cross-language cert
(JS/Dart also defer these).

## Tier 5 — Kernel / pipeline aggregators (forbidden 23–28; pull the whole stack)

| count | APIs |
| ---: | --- |
| **~9** | `get_runtime_kernel`, `run_canonical_pipeline`, `analyze`, `compile_document`, `compile_repository`, `query_repo`, `extract_recursive`, `universal_extract`, `run_autonomous_extraction` |

These import the entire `webweavex` package / kernel, so they unblock **only after** Tiers 2+3 are
resolved. Lowest ROI until then.

## Special (4)

`RuntimeKernel`, `__version__`, `version`, `crawl_async`/`extract_async` (async aliases) — version
constants / async wrappers; handled separately.

## Ranked plan

1. **Tier 1** (S20, +2 → 92) — finish the clean sweep.
2. **Tier 2 bs4-decouple** (Phase B, +~9 → ~101) — highest APIs/effort; one upstream lazy-import.
3. **Tier 3 lxml Soup engine** (Phase C, +~6, and unblocks much of Tier 5 → ~120s).
4. **Tier 5** aggregators fall out as Tiers 2+3 land.
5. **Tier 4** Playwright/platform harness last (or remain honest-Deferred, matching JS/Dart).
