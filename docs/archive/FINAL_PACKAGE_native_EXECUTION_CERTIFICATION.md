# FINAL PACKAGE NATIVE EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 31 |
| PASS | 14 |
| FAIL | 17 |
| UNTESTED | 0 |
| Hash mismatches | 3 |
| State mismatches | 4 |

## Behavioral mismatches

- `core/native/electron/electron_cdp_engine.py` — output_or_state_mismatch
- `core/native/electron/electron_hash_engine.py` — output_or_state_mismatch
- `core/native/electron/electron_ipc_engine.py` — py=None js='tsx' is not recognized as an internal or external command,
operable program or batch file.

- `core/native/electron/electron_route_engine.py` — py=None js='tsx' is not recognized as an internal or external command,
operable program or batch file.

- `core/native/electron_runtime_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/native/native_checkpoint_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/native/native_interaction_engine.py` — py=None js=ALLOWED_ACTIONS.includes is not a function
- `core/native/native_memory_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\determinism\normalization.ts
- `core/native/native_runtime_orchestrator.py` — py=None js=Transform failed with 3 errors:
C:\Projects\WebWeaveX\src\synchronization\runtimeSyncOrchestrator.ts:31:170: ERROR: Cannot use "||" with "??" without parentheses
C:\Projects\WebWeaveX\src\synchronization\runtimeSyncOrchestrator.ts:31:267: ERROR: Cannot use "||" with "??" without parentheses
C:\Projects\WebWeaveX\src\synchronization\runtimeSyncOrchestrator.ts:31:368: ERROR: Cannot use "||" with "??" without parentheses
- `core/native/native_stream_engine.py` — output_or_state_mismatch
- `core/native/native_terminal_engine.py` — py=None js=parts.encode is not a function
- `core/native/native_ui_graph_engine.py` — py=None js=bucket is not defined
- `core/native/native_vm_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/native/native_window_engine.py` — py=None js=sys is not defined
- `core/native/platform/linux_atspi_runtime.py` — py=None js=sys is not defined
- `core/native/platform/macos_ax_runtime.py` — py=None js=sys is not defined
- `core/native/platform/windows_uia_runtime.py` — py=None js=sys is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
