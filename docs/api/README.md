# Public API

## Package entry

```python
import webweavex
webweavex.__version__  # "2.0.0"
```

## Recommended ingress

```python
from webweavex import UniversalInput, run_canonical_pipeline
```

## Common operations

| Function | Purpose |
|----------|---------|
| `extract_web(url, **opts)` | Full browser runtime extraction |
| `extract_repository(path)` | Repository IR and graph inputs |
| `extract_document_runtime(text)` | Document runtime |
| `extract_native(**opts)` | Native / Electron / terminal snapshots |
| `run_canonical_pipeline(inp)` | Single canonical path |
| `compute_global_runtime_fingerprint(payload)` | Cross-run stable digest |
| `validate_replay_equivalence(a, b)` | Graph + fingerprint parity |
| `encrypt_value` / `decrypt_value` | Kaalka field crypto |
| `save_encrypted_session` / `load_encrypted_session` | Session blobs |

## Optional

- `webweavex.plugins` — fail-safe task plugins (rule-based default)
- `webweavex.api.api.run` — legacy compiler-mode HTTP-style API over `core/full_pipeline` (not canonical; omitted from coverage gate)
