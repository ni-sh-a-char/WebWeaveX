# JAVA_PLAYWRIGHT_VERDICT

**Phase-3 audit (Session 28). Verdict: SPLIT — 4 of 5 "Playwright" APIs are PORTABLE and were
CERTIFIED this session via a browser-free stub-page contract; `extract_web` alone is browser-runtime
required.** Python canon `9625f4a`.

## Method
Question posed by the directive: *can the outputs be reproduced without a live browser runtime?*
Answer, per runtime call graph + empirical execution: **yes, for four of them.** The engines never
call live Playwright on their observable path — they read only a page's `_test_*` attributes (or
return empty when absent / page is `null`). The real `page.evaluate`/`page.click`/… calls are guarded
behind `hasattr(page, …)` and are side-effect only; they never reach the serialized output.

## Certified this session (4 APIs → contributed to 97→105)
| API | Engine | Observable frontier | Java |
|-----|--------|---------------------|------|
| `capture_websocket_frames` | reads `page._test_websocket_frames`; pure `make_stream_event` + `normalize_stream_events` | events list (sorted) | `StreamingRuntime#captureWebsocketFrames` |
| `capture_dom_mutations` | reads `_test_dom_mutations` + `_test_html`; `compute_kaalka_hash` (certified) | mutations/events + `dom_hash` | `StreamingRuntime#captureDomMutations` |
| `extract_infinite_scroll` | `_test_scroll()` loop; DOM hash via `_test_dom_hash`/`_test_html` | scrolls/chunks/stable flag | `InfiniteScroll#extractInfiniteScroll` |
| `replay_interactions` | output = pure `record_interaction(...)`; handlers side-effect only | replay log | `InteractionReplay#replayInteractions` |

Evidence: `golden_vectors_s28.json` (24 vectors incl. `track_websocket_connections` support) —
byte-identical `stable_serialize` + `compute_kaalka_hash` to canonical Python, stub pages mirroring
the canonical Python unit-test doubles (`_ScrollPage`, `_WsPage`, `_DomPage`). Tests:
`CrossLanguageParityS28Test`. All green under `mvn verify`.

## `extract_web` — browser-runtime REQUIRED (blocked)
### A. Concrete runtime
`extract_web(url) → render_page(url)`: if `sync_playwright is None` → `{available:False,
reason:"playwright_missing", bounded:True}`; else `chromium.launch(headless=True)`, `page.goto(url,
wait_until="networkidle")`, `html = page.content()`.
### B. Observable dependency
The entire payload (`dom`, `extraction`, `browser_ir`, `global_runtime_fingerprint`, …) derives from
`page.content()` — live headless-Chromium rendering after network-idle.
### C. Why Java cannot reproduce it
Live browser rendering is non-deterministic and platform-coupled; there is no pure-Java equivalent of
a Chromium render. The offline bail-out (`{available:False, reason:"playwright_missing", url, …}`) is
deterministic but is *not* the extraction behavior the API exists to provide — certifying only the
unavailable path would misrepresent parity.
### D. Frontier reduction
The four siblings reduced because their observable output is independent of the live page (it is the
`_test_*` data). `extract_web` has no such reduction: its output *is* the live render. (The html.parser
engines it uses — `reconstruct_dom`, `extract_semantic_content` — run only on a live page and are never
reached offline; they are not lxml.)

## Verdict
`capture_websocket_frames`, `capture_dom_mutations`, `extract_infinite_scroll`, `replay_interactions`
= **PORTABLE, CERTIFIED (S28)**. `extract_web` = **browser-runtime required (blocked)**; unblock lever
= add a deterministic `html=` snapshot contract (as `run_application_cognition` did in S26).
