# Cross-Language Deterministic Parity Specification

**Version:** `webweavex-formula+kaalka@5.0.0`  
**Branches:** `javascript` (reference implementation) · `python` (must conform to this spec)  
**Crypto substrate:** [`kaalka@5.0.0`](https://www.npmjs.com/package/kaalka) (npm registry only — no local forks)

---

## What this spec guarantees

When two runtimes implement **every step below identically**, they produce:

| Output | Guarantee |
|--------|-----------|
| `computeDeterministicHash(value)` | **Identical** SHA-256 hex digest |
| `stableSerialize(value)` | **Identical** UTF-8 string |
| `deriveKaalkaTimeKey(key)` | **Identical** `H:MM:SS` time key |
| `encryptValue` / `decryptValue` | **Identical** base64 ciphertext (round-trip) |

## What this spec does **not** claim

- **Not** “same ciphertext” unless Python uses **this** formula (not legacy `kaalka_runtime_engine` v2 byte-XOR + hex).
- **Not** “perfect crypto parity” with wall-clock Kaalka CLI encryption (non-deterministic without explicit `time_key`).
- **Not** raw HTML equality for replay — only **stabilized** DOM / graph / fingerprint equivalence.

---

## Canonical pipeline

```text
normalizeRuntimeValue (strings)
        ↓
stableSerialize (objects → canonical JSON string)
        ↓
Buffer.from(payload, "utf8")          ← mandatory UTF-8
        ↓
deriveKaalkaTimeKey(encryption_key)   ← pure SHA-256 scan, no Date.now()
        ↓
kaalka@5._proc(bytes, encrypt=true)   ← byte path only (not _encryptMessage)
        ↓
base64(ciphertext_bytes)
```

**Hash-only path** (no Kaalka encrypt):

```text
stableSerialize(value) → UTF-8 → SHA-256 → lowercase hex
```

---

## Step 1 — `normalizeRuntimeValue`

Applied to **string** inputs before serialization or direct hashing.

| Rule | Behavior |
|------|----------|
| Unicode | NFKC (`String.normalize("NFKC")` / `unicodedata.normalize("NFKC")`) |
| Line endings | `\r\n` and `\r` → `\n` |
| Trailing whitespace | Strip Unicode whitespace at end only (`\s+$`) |
| Surrogates / emoji | Preserved; must round-trip via UTF-8 |

**Example:**

```text
"café\r\n"  →  "café"
"a\r\n"     →  "a"        (trailing LF stripped as whitespace)
```

---

## Step 2 — `stableSerialize`

| Input type | Behavior |
|------------|----------|
| `string` | `normalizeRuntimeValue(string)` |
| `object` | `fast-json-stable-stringify(stableSortKeys(obj))` |
| `number` | JSON number rules (no `-0` special case in stringify lib) |
| `null` | JSON `null` |
| Arrays | Order preserved; elements recursively sorted if objects |

### Volatile key stripping (`stableSortKeys`)

These keys are **omitted** at every object level:

`timestamp`, `created_at`, `updated_at`, `nonce`, `request_id`, `csrf`, `generated_at`, `runtime_id`, `random`, `uuid`

### Graph ordering

Runtime graphs use `RuntimeGraphContract.normalize`:

- Nodes sorted by `id|type|name`
- Edges sorted by `source|target|type` (aliases `from`/`to` accepted)

---

## Step 3 — UTF-8 encoding

```ts
const bytes = Buffer.from(stableSerialize(value), "utf8");
```

**Forbidden:** `latin1`, BMP-only string ops, `JSON.stringify` without prior `stableSortKeys`.

---

## Step 4 — `deriveKaalkaTimeKey` (pure, replay-safe)

No system clock. No `Date.now()`. No randomness.

```text
digest = SHA256( normalizeRuntimeValue(encryption_key) as UTF-8 )
for i in 0 .. len(digest)-3:
    candidate = f"{digest[i] % 12}:{digest[i+1] % 60}:{digest[i+2] % 60}"
    if kaalka_v5_byte_roundtrip(candidate, probe_utf8):
        return candidate
return first working fallback in ["12:0:0", "12:34:56"]
```

**Probe payload** (must match across languages):

```text
UTF-8 bytes: 0x00, 0x7F, 0xFF, "🚀probe"
```

**Why probing:** Kaalka v5 `_encryptMessage` is **not** reversible for all clock tuples; WebWeaveX uses **`_proc` byte transform only**.

### Kaalka v5 `_proc` (byte transform)

For each byte index `idx` with clock `(h, m, s)`:

```text
key = (h * 3600 + m * 60 + s) || 1
offset = (key + idx) % 256
encrypt: (byte + offset) % 256
decrypt: (byte - offset + 256) % 256
```

`_setTime(time_key)` parses `H:MM:SS` (or `MM:SS`, `SS` variants) into `h % 12`, `m`, `s`.

---

## Step 5 — Base64 transport

Ciphertext on the wire is **always** standard base64 of raw `_proc` output bytes.

---

## DOM stabilization (replay layer)

Separate from crypto; used for `computeStableDomHash`:

- UUIDs → `uuid-stabilized`
- ISO timestamps → `timestamp-stabilized`
- Strip `data-react*`, `data-v-*`, `ng-*`, `_ngcontent*`, `_nghost*`, `nonce="..."`
- Remove HTML comments
- Collapse whitespace

Replay equivalence compares **hashes of stabilized DOM**, not raw HTML.

---

## Replay equivalence

`validateReplayEquivalence(original, replayed)` checks:

1. Normalized runtime graph hash
2. Global runtime fingerprint
3. Browser `runtime_identity` (when present)
4. Stabilized DOM hash (when `dom_snapshot` / `dom_html` present)

---

## Failure cases

| Failure | Symptom |
|---------|---------|
| Python still on v2 hex XOR | Hash may match; **ciphertext differs** |
| Using `_encryptMessage` | Unicode / emoji corruption |
| Wrong encoding | Latin1 mojibake in JSON decrypt |
| Wall-clock Kaalka | Non-deterministic ciphertext |
| Skipping volatile key strip | Graph hash drift |

---

## Validation artifacts

```text
validation/parity/
  js_vectors.json
  python_vectors.json
  parity_report.md
```

Generate: `npm run validate:parity`

---

## Architecture diagram

```mermaid
flowchart LR
  A[Runtime Value] --> B[normalizeRuntimeValue]
  B --> C[stableSerialize]
  C --> D[UTF-8 bytes]
  D --> E[deriveKaalkaTimeKey]
  E --> F[kaalka@5._proc]
  F --> G[base64]
  C --> H[SHA-256 hash]
```

---

## Limitations (honest)

1. **Python `python` branch** must migrate from legacy `kaalka_encrypt_bytes` to this spec for byte-identical ciphertext.
2. Kaalka npm package is time-oriented by design; WebWeaveX **pins** determinism via derived `time_key` + `_proc`.
3. Floating-point JSON edge cases depend on `fast-json-stable-stringify` / Python `json.dumps(sort_keys=True)` alignment — document any drift in parity reports.
