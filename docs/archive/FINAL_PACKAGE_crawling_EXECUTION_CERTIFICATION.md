# FINAL PACKAGE CRAWLING EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 34 |
| PASS | 21 |
| FAIL | 9 |
| UNTESTED | 4 |
| Hash mismatches | 1 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/crawling/advanced/__init__.py` — barrel_export_mismatch:['schedule']
- `core/crawling/advanced/incremental_crawl_engine.py` — py=None js=(c - p) is not iterable
- `core/crawling/crawler_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\crawling\crawlerEngine.ts:36:12: ERROR: The symbol "link" has already been declared
- `core/crawling/dedup_engine.py` — py=None js=urlsplit is not defined
- `core/crawling/intelligence/__init__.py` — barrel_export_mismatch:['semantic_priority', 'adaptive_recursion', 'dedup_frontier', 'rank_frontier', 'canonical_paths']
- `core/crawling/intelligence/adaptive_recursion_engine.py` — output_or_state_mismatch
- `core/crawling/recursion_engine.py` — py=AttributeError: 'str' object has no attribute 'allow' js=budget.allow is not a function
- `core/crawling/semantic_recursion_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\crawling\crawlerEngine.ts:36:12: ERROR: The symbol "link" has already been declared
- `core/crawling/streaming_crawler.py` — py=None js=js probe timeout after 60s

## UNTESTED

- `core/crawling/advanced/canonical_engine.py` — no_python_functions
- `core/crawling/advanced/pagination_engine.py` — no_python_functions
- `core/crawling/crawl_budget_engine.py` — no_python_functions
- `core/crawling/queue_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
