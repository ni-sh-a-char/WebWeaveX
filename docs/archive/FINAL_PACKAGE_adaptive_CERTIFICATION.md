# FINAL PACKAGE ADAPTIVE EXECUTION CERTIFICATION

**Measured:** 2026-06-04T13:07:23.021073+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 21 |
| PASS | 12 |
| FAIL | 9 |
| UNTESTED | 0 |
| Hash mismatches | 3 |
| State mismatches | 3 |

## Behavioral mismatches

- `core/adaptive/adaptive_recovery_engine.py` — output_or_state_mismatch
- `core/adaptive/adaptive_runtime_orchestrator.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/adaptive/extraction_fallback_engine.py` — py=None js=Cannot read properties of undefined (reading 'text')
- `core/adaptive/extraction_memory_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/adaptive/infinite_scroll_recovery_engine.py` — output_or_state_mismatch
- `core/adaptive/modal_recovery_engine.py` — output_or_state_mismatch
- `core/adaptive/replay_alignment_engine.py` — py=None js=Cannot read properties of null (reading 'every')
- `core/adaptive/runtime_adaptation_engine.py` — py=None js=Cannot read properties of undefined (reading 'text')
- `core/adaptive/selector_healing_engine.py` — py=None js=Cannot read properties of undefined (reading 'text')

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
