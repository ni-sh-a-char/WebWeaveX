# FINAL REPOSITORY PURIFICATION REPORT

## Deleted paths

- (already purged in prior pass)

## Archived reports


## Canonical architecture

- Pipeline: `core/kernel/runtime_pipeline.py`
- Contracts: `core/contracts/`
- Determinism: `core/determinism/global_runtime_fingerprint.py`
- Replay: `core/replay/replay_equivalence_engine.py`
- Crypto: `core/crypto/kaalka_runtime_engine.py` only

## Dependency cleanup

- Removed legacy shim imports (`core/*_engine.py` → `core/legacy`)
- Lazy `core/ir/__init__.py` prevents parser cycles