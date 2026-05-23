# Cross-Language Parity Report

**Algorithm:** `webweavex-formula+kaalka@5.0.0`
**Kaalka npm:** `5.0.0`
**Generated:** 2026-05-23T15:40:14.656Z

## JavaScript self-consistency

✅ **PASS** — all vectors decrypt and re-encrypt deterministically

## Python lockstep

✅ **PASS** — hash and ciphertext match reference vectors

## Honest limitations

- Identical ciphertext requires same UTF-8 pipeline, `deriveKaalkaTimeKey`, and `kaalka._proc` on both runtimes.
- Legacy Python `kaalka_runtime_engine` (byte-XOR hex) **will not** match until migrated.

## Results

```json
{
  "selfOk": true,
  "needsReseed": false,
  "crossLangMatch": true,
  "results": [
    {
      "id": "probe-1",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "probe-2",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "unicode",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "emoji",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "crlf",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "session",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "nested-object",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "graph",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "array",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "dom",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    },
    {
      "id": "memory-graph",
      "hash_match": true,
      "encrypt_match": true,
      "decrypt_ok": true,
      "deterministic": true
    }
  ]
}
```