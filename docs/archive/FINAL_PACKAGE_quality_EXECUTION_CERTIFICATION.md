# FINAL PACKAGE QUALITY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 7 |
| PASS | 3 |
| FAIL | 4 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/quality/__init__.py` — barrel_export_mismatch:['score_extraction', 'score_semantic_confidence', 'compute_redundancy', 'resolve_conflicts', 'source_consensus']
- `core/quality/redundancy_engine.py` — output_or_state_mismatch
- `core/quality/semantic_confidence_engine.py` — output_or_state_mismatch
- `core/quality/source_consensus_engine.py` — py=None js=k is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
