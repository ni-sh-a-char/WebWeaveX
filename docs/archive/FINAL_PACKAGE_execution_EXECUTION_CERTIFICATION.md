# FINAL PACKAGE EXECUTION EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 21 |
| PASS | 8 |
| FAIL | 13 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/execution/runtime_action_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/execution/runtime_checkpoint_engine.py` — py=None js=Path is not defined
- `core/execution/runtime_coordination_engine.py` — py=None js=route is not defined
- `core/execution/runtime_execution_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/execution/runtime_execution_orchestrator.py` — py=TypeError: unhashable type: 'dict' js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/execution/runtime_permissions_engine.py` — output_or_state_mismatch
- `core/execution/runtime_recovery_engine.py` — py=None js=action is not defined
- `core/execution/runtime_rollback_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/execution/runtime_sandbox_engine.py` — output_or_state_mismatch
- `core/execution/runtime_simulation_engine.py` — py=None js=(prior || []) is not iterable
- `core/execution/runtime_state_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/execution/runtime_transaction_engine.py` — py=None js=payload.encode is not a function
- `core/execution/runtime_transition_engine.py` — py=TypeError: unhashable type: 'dict' js=_VALID_TRANSITIONS.includes is not a function

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
