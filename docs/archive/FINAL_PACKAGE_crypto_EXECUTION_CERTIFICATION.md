# FINAL PACKAGE CRYPTO EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 12 |
| PASS | 5 |
| FAIL | 6 |
| UNTESTED | 1 |
| Hash mismatches | 2 |
| State mismatches | 2 |

## Behavioral mismatches

- `core/crypto/cross_language_normalizer.py` — output_or_state_mismatch
- `core/crypto/kaalka_engine.py` — py=TypeError: unsupported operand type(s) for ^: 'str' and 'str' js=hex_fingerprint is not defined
- `core/crypto/kaalka_key_engine.py` — py=None js=normalized.encode is not a function
- `core/crypto/kaalka_v5_proc.py` — py=ValueError: invalid literal for int() with base 10: 'probe' js=None
- `core/crypto/kaalka_wrapper.py` — py=TypeError: unsupported operand type(s) for ^: 'str' and 'int' js=bytes is not defined
- `core/crypto/serializer_v3.py` — output_or_state_mismatch

## UNTESTED

- `core/crypto/kaalka_hash_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
