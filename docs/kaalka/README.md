# Kaalka

Kaalka is WebWeaveX’s **deterministic persistence crypto layer** for runtime state.

## Usage

```python
from webweavex import encrypt_value, decrypt_value, encrypt_session_state, decrypt_session_state
```

Same plaintext + key → same ciphertext (auditable, replay-friendly).

## Integration points

- Workflow, execution, distributed, semantic, sync, and session stores
- Pattern: canonical JSON → `encrypt_value` → wrapper file with `"algorithm": "kaalka"`

## Cross-language validation

Reference fixtures and scripts:

```
validation/kaalka_cross_language/
```

Run:

```bash
python validation/kaalka_cross_language/validate_cross_language.py
```
