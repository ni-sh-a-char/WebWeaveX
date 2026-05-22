# Architecture

## Canonical pipeline

All production ingress should use:

```python
from webweavex import UniversalInput, run_canonical_pipeline

run_canonical_pipeline(UniversalInput(source="...", source_type="web"))
```

Implementation: `core/kernel/runtime_pipeline.py`

## Flow

1. **UniversalInput** — typed ingress (`source`, `source_type`, `url`, `path`, session, options)
2. **Ingestion** — `core/ingestion/universal_ingestion_engine.py`
3. **Extraction** — web / repository / document / multimodal / text
4. **RuntimeKernel** — semantic, synchronization, memory, execution, reconstruction
5. **Unified runtime graph** — normalized nodes and edges
6. **pipeline_hash** — deterministic digest of graph payload

## Specialized engines (called from pipeline or public API)

- Browser: `core/browser/universal_web_extraction_engine.py`
- Native: `core/native/native_runtime_orchestrator.py`
- Connectors: `core/connectors/*`
- Memory / sync / workflows: respective `core/<phase>/` orchestrators

## Forbidden patterns

- Shadow orchestrators parallel to `run_canonical_pipeline`
- `uuid4`, `random`, pickle persistence for runtime state
- Plaintext operational checkpoints

See archived lock report: `docs/archive/WEBWEAVEX_v2_ARCHITECTURE_LOCK_REPORT.md`
