# Runtime Kernel

`core/kernel/` is the single canonical orchestration layer for WebWeaveX.

## Role

The kernel **routes** extraction phases — it does not duplicate phase logic. Each phase remains in its canonical package (`core/semantic/`, `core/memory/`, etc.) and is invoked through deterministic bridges.

## Key modules

| Module | Purpose |
|--------|---------|
| `runtime_kernel.py` | `RuntimeKernel.run_pipeline()` |
| `runtime_bus.py` | Ordered event bus (bounded) |
| `runtime_scheduler.py` | Deterministic phase scheduling |
| `runtime_*_bridge.py` | Phase adapters |
| `runtime_policy.py` | Bounds enforcement |
| `runtime_boundary.py` | Payload size limits |

## Example

```python
from core.kernel import RuntimeKernel

kernel = RuntimeKernel("browser")
result = kernel.run_pipeline(sources={...}, tick=0)
```

## Unified IR

Pipeline output includes `unified_ir` from `core/ir/unified_runtime_ir.py` — a merged view of all phase IRs for graph compilation.
