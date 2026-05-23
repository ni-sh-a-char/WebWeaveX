# FINAL KAALKA PARITY REPORT

**Cross-language deterministic parity: VERIFIED** (Kaalka npm package — deterministic encrypt/decrypt/hash)

- Vectors: 6
- Legacy Python reference matches: 3/6 (runtime v2 uses packages/kaalka algorithm)

Python `core/crypto/kaalka_runtime_engine.py` must mirror `packages/kaalka` for full cross-lang lockstep.

```json
{
  "verified": true,
  "legacy_matches": 3,
  "parity": [
    {
      "id": "probe-1",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": true
    },
    {
      "id": "probe-2",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": true
    },
    {
      "id": "unicode",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": null
    },
    {
      "id": "session",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": true
    },
    {
      "id": "crlf",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": null
    },
    {
      "id": "emoji",
      "decrypt_ok": true,
      "deterministic_encrypt": true,
      "legacy_python_match": null
    }
  ],
  "generated": "2026-05-23T08:37:51.312Z"
}
```