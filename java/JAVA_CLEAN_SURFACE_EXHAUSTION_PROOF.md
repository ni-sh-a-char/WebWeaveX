# JAVA_CLEAN_SURFACE_EXHAUSTION_PROOF

**Phase 6 — conclusive exhaustion proof (machine-derived, S20).** Live state: **92/128 proven,
36 remaining.** Every remaining API was traced (relative-aware) **and runtime-imported** in
canonical Python `9625f4a`; serialization, filesystem, and page/runtime coupling audited per API.

## Result: the dependency-clean, page-free, byte-exact surface is EXHAUSTED.

After the memory orchestrator (`run_runtime_memory`, `run_memory_for_extraction` — S20), **zero**
remaining APIs are simultaneously (a) 0-forbidden, (b) page-free, (c) FS-fixture-free, and
(d) byte-exact-serializable. Every one of the 36 is blocked by exactly one of the categories below.

## Per-API classification (all 36 remaining)

### bs4-coupled (Tier 2) — 9
`query_documents`, `query_semantics`, `reason_semantically`, `run_semantic_runtime`,
`run_semantic_for_extraction`, `extract_multimodal`, `ingest_input`, `heal_selector`,
`run_application_cognition`.
**Justification:** trace shows forbidden=1–4 reaching BeautifulSoup via the semantic/evidence
stack. **Blocking dependency:** bs4. **Cost:** unlocked en masse by one upstream lazy-import
(see `JAVA_BS4_DECOUPLE_PLAN.md`).

### lxml / HTML-extraction-pipeline (Tier 3) — 6
`extract`, `extract_docs`, `extract_repo`, `stream_extract`, `extract_web`, `crawl`.
**Justification:** forbidden≈5–13 via `core.extract.pipeline` (bs4 **and** lxml). **Blocking
dependency:** a deterministic lxml/bs4-parity Soup engine. **Cost:** multi-session Soup engine.

### Playwright / platform / filesystem-coupled (Tier 4) — 7
`capture_dom_mutations`, `capture_websocket_frames`, `extract_infinite_scroll`,
`replay_interactions` (live `page`); `extract_native`, `run_native_cognition` (`sys.platform`);
`extract_repository` (walks a real FS repo).
**Justification:** 0–6 forbidden but require a live Playwright page / OS / on-disk repo — no static
byte-exact oracle. **Blocking dependency:** a mock-page / platform / fixture-repo harness.
**Cost:** harness per sub-family; honest-Deferred in JS/Dart too.

### Kernel / pipeline aggregators (Tier 5) — 9
`get_runtime_kernel`, `run_canonical_pipeline`, `analyze`, `compile_document`, `compile_repository`,
`query_repo`, `extract_recursive`, `universal_extract`, `run_autonomous_extraction`.
**Justification:** forbidden=23–28 — they import the whole `webweavex`/kernel stack. **Blocking
dependency:** all of Tiers 2+3. **Cost:** falls out for free once Tiers 2+3 land.

### Special (5)
`RuntimeKernel`, `__version__`, `version` (version/kernel constants), `crawl_async`,
`extract_async` (async wrappers over Tier-2/3 sync APIs — inherit their blockers).

## Tally

| Tier | count |
| --- | ---: |
| 1 — clean | **0** (exhausted) |
| 2 — bs4 | 9 |
| 3 — lxml | 6 |
| 4 — page/platform/FS | 7 |
| 5 — kernel aggregators | 9 |
| special | 5 |
| **total remaining** | **36** |

**Conclusion:** Phase A is complete at **92/128**. No further progress is possible without the
Phase-B bs4-decouple campaign (highest ROI), the Phase-C lxml Soup engine, or a Playwright/platform
harness. The clean surface is **conclusively exhausted**.
