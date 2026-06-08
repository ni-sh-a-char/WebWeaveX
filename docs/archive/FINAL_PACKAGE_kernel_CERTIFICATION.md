# FINAL PACKAGE KERNEL EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 22 |
| PASS | 6 |
| FAIL | 16 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/kernel/runtime_bus.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/kernel/runtime_connector_bridge.py` — py=None js=runLiveForExtraction is not defined
- `core/kernel/runtime_context.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/kernel/runtime_dispatcher.py` — py=TypeError: 'dict' object is not callable js=kwargs is not defined
- `core/kernel/runtime_execution_bridge.py` — py=TypeError: unhashable type: 'dict' js=runExecutionForExtraction is not defined
- `core/kernel/runtime_graph_bridge.py` — py=None js=buildRuntimeGraph is not defined
- `core/kernel/runtime_identity_bridge.py` — py=ModuleNotFoundError: No module named 'core.identity.browser_identity_engine' js=buildBrowserIdentity is not defined
- `core/kernel/runtime_kernel.py` — py=None js=Cannot read properties of undefined (reading 'runtime_type')
- `core/kernel/runtime_lifecycle.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/kernel/runtime_memory_bridge.py` — py=None js=runMemoryForExtraction is not defined
- `core/kernel/runtime_pipeline.py` — py=AttributeError: 'str' object has no attribute 'source_type' js=Cannot read properties of undefined (reading 'startsWith')
- `core/kernel/runtime_registry.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/kernel/runtime_scheduler.py` — py=None js=phase is not defined
- `core/kernel/runtime_semantic_bridge.py` — py=None js=runSemanticForExtraction is not defined
- `core/kernel/runtime_state.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/kernel/runtime_sync_bridge.py` — py=None js=runSyncForExtraction is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
