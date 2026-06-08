# FINAL PACKAGE CAUSALITY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 21 |
| PASS | 12 |
| FAIL | 9 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/causality/causal_checkpoint_engine.py` — py=None js=Path is not defined
- `core/causality/causal_memory_engine.py` — py=None js=Path is not defined
- `core/causality/causality_orchestrator.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/causality/cross_runtime_alignment_engine.py` — py=None js=e is not defined
- `core/causality/distributed_causality_engine.py` — output_or_state_mismatch
- `core/causality/event_chain_engine.py` — output_or_state_mismatch
- `core/causality/notification_causality_engine.py` — py=None js=Cannot read properties of undefined (reading 'id')
- `core/causality/runtime_causality_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/causality/runtime_sequence_engine.py` — py=None js=event is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
