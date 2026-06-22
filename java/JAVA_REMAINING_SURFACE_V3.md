# JAVA_REMAINING_SURFACE_V3

**Exhaustion audit (Phase B, post-S25). 96 / 128 proven, 32 remaining.** Every remaining API
classified by **runtime frontier** (not import closure), per the method that resolved
query_documents (port) and query_semantics/reason_semantically (proven blocked).

## Tally

| Tier | count | certifiable? |
| --- | ---: | --- |
| 1 — portable, pending port | **~1–2** | yes |
| 2 — Python `ast` (CPython parser in output) | **~7** | condition-B (canon change) |
| 3 — lxml/bs4 HTML-parse (output bs4-dependent) | **~6** | Tier-C Soup engine |
| 4 — Playwright / platform / OCR / FS | **~7** | non-portable (proven) |
| 5 — kernel/pipeline aggregators | **~7** | unblock after 2+3 |
| special | **2** | version constants |

## Per-API classification

### Tier 1 — portable, pending (the live frontier)
- `run_application_cognition` — orchestrator with bs4 HTML engines; **needs empirical html=""
  frontier check** (may be portable like run_semantic_runtime). **Next candidate.**

### Tier 2 — Python `ast` (condition-B BLOCKED, proven)
`query_semantics`, `reason_semantically` (proven S24, `JAVA_AST_FRONTIER_*`), `compile_repository`,
`extract_repo`, `extract_repository`, `query_repo`, `analyze` — all embed
`compile_semantic_ast_ir` → `ast.parse` in observable output, OR are aggregators that do. CPython
AST fidelity for arbitrary source is non-portable.

### Tier 3 — lxml/bs4 HTML-parse (output bs4-DEPENDENT)
`extract`, `extract_docs`, `extract_web`, `crawl`, `crawl_async`, `stream_extract` — parse real HTML
and the parsed structure reaches the output (unlike the html="" contract). Need a deterministic
lxml/bs4-parity Soup engine (Tier C).

### Tier 4 — Playwright / platform / OCR / FS (non-portable, proven)
`capture_dom_mutations`, `capture_websocket_frames`, `extract_infinite_scroll`, `replay_interactions`
(live Playwright page); `extract_native`, `run_native_cognition` (`sys.platform`);
`extract_multimodal`, `ingest_input` (OCR / FS). No static byte-exact oracle.

### Tier 5 — kernel/pipeline aggregators
`get_runtime_kernel`, `run_canonical_pipeline`, `compile_document`, `extract_recursive`,
`run_autonomous_extraction`, `universal_extract`, `extract_async` — import/run the whole stack;
unblock only after Tiers 2+3.

### Special (2)
`RuntimeKernel`, `__version__`/`version` — kernel/version constants.

## Conclusion

The portable, byte-exact, non-AST, non-bs4-output surface is **nearly exhausted**:
`run_application_cognition` is the one remaining candidate (pending an empirical html="" frontier
check, S26). After it, **every remaining API has a port path (Tier-C Soup engine) or a formal
blocker proof** (Python `ast`, Playwright, platform, OCR, FS). Convergence toward the success
condition (128/128 or fully-proven-blocked) continues.
