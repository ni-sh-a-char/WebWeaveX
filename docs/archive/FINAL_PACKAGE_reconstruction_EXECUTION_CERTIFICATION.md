# FINAL PACKAGE RECONSTRUCTION EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 20 |
| PASS | 3 |
| FAIL | 17 |
| UNTESTED | 0 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/reconstruction/application_reconstruction_engine.py` — py=None js=workflows.includes is not a function
- `core/reconstruction/browser_reconstruction_engine.py` — py=None js=index is not defined
- `core/reconstruction/runtime_checkpoint_reconstruction.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/reconstruction/runtime_clone_engine.py` — py=None js=copy is not defined
- `core/reconstruction/runtime_fabrication_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/reconstruction/runtime_identity_reconstruction.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/reconstruction/runtime_memory_reconstruction.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/reconstruction/runtime_reconstruction_engine.py` — py=None js=canonical.encode is not a function
- `core/reconstruction/runtime_reconstruction_orchestrator.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/reconstruction/runtime_recovery_reconstruction.py` — output_or_state_mismatch
- `core/reconstruction/runtime_replay_builder.py` — py=None js=index is not defined
- `core/reconstruction/runtime_snapshot_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/reconstruction/runtime_state_rebuilder.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/reconstruction/runtime_timeline_engine.py` — py=None js=items is not defined
- `core/reconstruction/runtime_topology_reconstruction.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/reconstruction/runtime_validation_engine.py` — py=None js=Cannot read properties of null (reading 'every')
- `core/reconstruction/session_reconstruction_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
