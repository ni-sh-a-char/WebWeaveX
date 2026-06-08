# FINAL PACKAGE PERFORMANCE EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 8 |
| PASS | 4 |
| FAIL | 4 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/performance/__init__.py` — barrel_export_mismatch:['budgeted_chunks', 'memory_budget', 'incremental_parse', 'lazy_extract', 'parser_pool']
- `core/performance/chunk_budget_engine.py` — py=None js=i is not defined
- `core/performance/streaming_buffer_engine.py` — py=ValueError: range() arg 3 must not be zero js=i is not defined
- `core/performance/streaming_engine.py` — py=None js=i is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
