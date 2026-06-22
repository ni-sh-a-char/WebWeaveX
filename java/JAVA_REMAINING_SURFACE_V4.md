# JAVA_REMAINING_SURFACE_V4

**Exhaustion audit (post-S26). 97 / 128 proven, 31 remaining.** Every remaining API classified by
runtime frontier — **no "unknown" category**.

## Tally

| Category | count |
| --- | ---: |
| parity-proven | 97 |
| portable pending | **0** |
| AST blocked (condition-B) | 8 |
| extraction-engine blocked (lxml/bs4-output) | 6 |
| Playwright blocked | 4 |
| OCR blocked | 2 |
| platform blocked | 2 |
| kernel aggregator | 7 |
| special (version) | 2 |

## Per-API classification (all 31 remaining)

### AST blocked — CPython `ast.parse` in observable output (condition-B, proven S24)
`query_semantics`, `reason_semantically`, `compile_repository`, `extract_repo`,
`extract_repository`, `query_repo`, `analyze`, `extract_recursive` — each embeds (directly or via
aggregation) `compile_semantic_ast_ir` → `ast.parse`, whose `lineno`/`end_lineno`/`args`/`bases`
reach the output (see `JAVA_AST_FRONTIER_*`). Non-portable for arbitrary source.

### Extraction-engine blocked — lxml/bs4 parsed structure reaches output (Tier-C Soup engine)
`extract`, `extract_docs`, `extract_web`, `crawl`, `crawl_async`, `stream_extract` — parse real
HTML and the parsed DOM/structure is observable (not the html="" contract). Need a deterministic
lxml/bs4-parity Soup engine.

### Playwright blocked — live page (non-portable)
`capture_dom_mutations`, `capture_websocket_frames`, `extract_infinite_scroll`,
`replay_interactions` — read a live Playwright `page`; no static byte-exact oracle.

### OCR blocked
`extract_multimodal`, `ingest_input` — image OCR (Tesseract) / multimodal.

### platform blocked — sys.platform native runtime
`extract_native`, `run_native_cognition`.

### kernel aggregator — import/run the whole stack (unblock after AST + extraction)
`get_runtime_kernel`, `run_canonical_pipeline`, `compile_document`, `universal_extract`,
`run_autonomous_extraction`, `extract_async`, `RuntimeKernel`.

### special (version constants)
`__version__`, `version`.

## Conclusion

**The portable-pending category is now EMPTY** — `run_application_cognition` (the last candidate)
is certified (S26). Every remaining API now carries a definite classification: a **port path** (the
Tier-C lxml Soup engine, ~6 APIs + much of the kernel-aggregator fallout) or a **formal blocker
proof** (CPython `ast`, Playwright, OCR, platform). The next strategic decision is the Tier-C Soup
engine (a deterministic lxml/bs4-parity HTML parser) — the single lever that unblocks the extraction
family and the aggregators that depend on it. The condition-B (`ast`), Playwright, OCR, and platform
sets are non-portable without a Python-canon change.
