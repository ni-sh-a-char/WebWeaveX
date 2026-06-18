# JAVA_SESSION_CRYPTO_AUDIT

**Phase 3 (mandatory) — dedicated audit of the session-crypto APIs.** Implemented this slice;
this records the exact Python behavior, the required substrate, closure size, and reuse value.

## APIs & exact Python behavior

### `encrypt_session_state(session, key)` — `core/crypto/kaalka_session_engine.py:14`
```
serialized = json.dumps(session, sort_keys=True, separators=(",",":"), ensure_ascii=False)[:10_000_000]
encrypted  = encrypt_value(serialized, key)         # {encrypted, algorithm, deterministic, bounded}
return {**encrypted, "payload_type": "session", "bounded": True}
```
Java: `PyJson.dumpsCompactUnicode(session)` + `Kaalka.encryptValueEnvelope(serialized, key)` +
`payload_type`. **Pure**, no FS. Byte-exact (the base64 ciphertext is deterministic — Kaalka
time-key is derived from `key`, no randomness).

### `decrypt_session_state(payload, key)` — `:34`
```
ciphertext = str(payload.get("encrypted", ""))
text       = str(decrypt_value(ciphertext, key).get("decrypted", ""))
session    = json.loads(text[:10_000_000])
return {"session": session, "algorithm": "kaalka", "deterministic": True, "bounded": True}
```
Java: `Kaalka.decryptValueEnvelope` + **`PyJsonParse.loads(text)`**. Pure, no FS. The
round-trip recovers the **NFKC-normalized** session (because `encrypt_value` runs
`stable_serialize` = NFKC over the JSON string before encryption) — Python and Java agree.

### `save_encrypted_session(path, session, key)` — `core/session/encrypted_session_store.py:13`
```
payload = encrypt_session_state(session, key)
Path(path).parent.mkdir(parents=True, exist_ok=True)
Path(path).write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")  # default seps, ascii
return {"saved": True, "path": str(Path(path)), "algorithm": "kaalka", "bounded": True}
```
**Filesystem.** Java: `PyJson.dumpsDefaultAscii(payload)` written via `Files.write`. The written
**file content is byte-identical** to Python; the returned `path` is `str(Path(path))`
(separator-sensitive — bare filenames are portable, matching the Session-4A R-2 note).

### `load_encrypted_session(path, key)` — `:36`
```
if not exists -> {"available": False, "session": <full empty shape>, "bounded": True}
payload = json.loads(read_text)           # corrupt -> {"available": False, "reason": str(exc)[:200], "session": <short shape>, "bounded": True}
decrypted = decrypt_session_state(payload, key)
return {"available": True, "session": decrypted.get("session", {}), "algorithm": "kaalka", "bounded": True}
```
**Filesystem + `json.loads`.** Java mirrors all three branches. The corrupt-file `reason` is
`str(exc)[:200]` — environment-specific (Java/Python exception text differs), so it is **excluded
from byte-exact comparison** (only the deterministic contract — `available:false` + the short
session shape — is asserted, like a path field).

## Required JSON substrate

| Direction | Python | Java (status) |
| --- | --- | --- |
| `json.dumps` (sort_keys, compact, ensure_ascii=False) | `encrypt_session_state` | `PyJson.dumpsCompactUnicode` — **existed** |
| `json.dumps` (sort_keys, default seps, ascii) | `save_encrypted_session` | `PyJson.dumpsDefaultAscii` — **existed** |
| **`json.loads`** | `decrypt_session_state`, `load_encrypted_session` | **`PyJsonParse` — BUILT THIS SLICE** |

`PyJsonParse` (JDK-only recursive-descent) matches CPython `json.loads`: object→LinkedHashMap
(insertion order), int→Long/BigInteger (unbounded), float→Double, NaN/Infinity accepted,
`\uXXXX` + surrogate pairs. Proven by 40 `json_loads` vectors (oracle = Python `json.loads`),
incl. malformed→raise (12 cases). 100% instruction coverage.

## Closure & reuse value

- Closure: 4–5 modules / 282–362 lines, **0 forbidden** (the rest is the proven foundation).
- **Reuse value (the reason this audit is mandatory):** `PyJsonParse` is the substrate every
  `decrypt_*`/`load_*` roundtrip API needs — ≈30 remaining APIs across
  `core.workflows`/`synchronization`/`causality`/`evolution_runtime`/`memory`/`identity`/
  `connectors`. Building it here removes that recurring blocker for all of them.

## Result

All 4 APIs implemented and parity-proven (37 cluster vectors + 40 substrate vectors = byte-exact
to Python). 27 → 31 proven. The substrate is the strategic deliverable.
