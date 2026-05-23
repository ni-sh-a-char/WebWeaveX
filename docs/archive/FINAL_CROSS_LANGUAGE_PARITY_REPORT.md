# FINAL CROSS-LANGUAGE PARITY REPORT

**Status:** VERIFIED

## Summary

| Gate | Result |
|------|--------|
| Normalization / serialization | PASS |
| Time-key derivation | PASS |
| Hash parity | PASS |
| Ciphertext parity | PASS |
| Python self-consistency | PASS |

## Per-vector results

```json
[
  {
    "id": "probe-1",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "probe-2",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "unicode",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "emoji",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "crlf",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "session",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "nested-object",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "graph",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "array",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "dom",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  },
  {
    "id": "memory-graph",
    "pass": true,
    "serialized": true,
    "time_key": true,
    "hash": true,
    "encrypted": true,
    "decrypt_ok": true,
    "deterministic": true
  }
]
```
