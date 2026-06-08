# FINAL PACKAGE INTEGRATIONS EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 9 |
| PASS | 0 |
| FAIL | 4 |
| UNTESTED | 5 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/integrations/__init__.py` — barrel_export_mismatch:['ProviderRegistry', 'CapabilityRegistry', 'supports_capability', 'augment_metadata']
- `core/integrations/augmentation_runtime.py` — py=None js=Class constructor CapabilityRegistry cannot be invoked without 'new'
- `core/integrations/capability_registry.py` — py=None js=Class constructor CapabilityRegistry cannot be invoked without 'new'
- `core/integrations/provider_router.py` — py=None js=Class constructor CapabilityRegistry cannot be invoked without 'new'

## UNTESTED

- `core/integrations/embedding_adapter_protocol.py` — no_python_functions
- `core/integrations/llm_adapter_protocol.py` — no_python_functions
- `core/integrations/provider_contracts.py` — no_python_functions
- `core/integrations/provider_registry.py` — no_python_functions
- `core/integrations/reasoning_adapter_protocol.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
