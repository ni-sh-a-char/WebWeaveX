# Replay and reconstruction

## Replay equivalence

```python
from webweavex import validate_replay_equivalence

report = validate_replay_equivalence(original_extraction, replayed_extraction)
# report["equivalent"] — graph, fingerprint, topology checks
```

Implementation: `core/replay/replay_equivalence_engine.py`

## Reconstruction

```python
from webweavex import run_reconstruction_runtime, reconstruct_runtime
```

Reconstruction orchestrator rebuilds runtime views from stored sources and validates bounded output.

## Determinism expectations

- Same ingestion bytes → same stabilized DOM hash
- Same graph inputs → same `pipeline_hash` / global fingerprint
- Live refetch of dynamic sites may differ; tests should use fixed HTML when asserting strict equality
