# WebWeaveX Canonical Runtime Specification

**Version:** 2.0.0  
**Status:** Source of truth for `python`, `javascript`, and `dart` branches  
**Algorithm:** `webweavex-formula+kaalka@5.0.0`

---

## 1. Identity

WebWeaveX is **deterministic runtime cognition infrastructure** for **humans and AI agents** operating on **authenticated operational systems**, with replay-safe continuity, runtime memory, cross-language parity, and reconstruction capability.

WebWeaveX is **not** a scraper, crawler, AGI product, auth-bypass toolkit, or LLM wrapper.

---

## 2. Runtime pipeline (canonical)

```text
UniversalInput
  → normalizeRuntimeValue / stableSerialize
  → deriveKaalkaTimeKey
  → kaalka@5.0.0 byte _proc + base64
  → runtime graph (canonical nodes/edges)
  → runtime memory fabric
  → reconstruction
  → validateReplayEquivalence
```

| Stage | Responsibility |
|-------|----------------|
| Normalization | NFKC, CRLF→LF, volatile key strip, stable key order |
| Serialization | Canonical JSON string for hashing/encryption |
| Crypto | UTF-8 bytes → time key → `_proc` → base64 |
| Graph | Sorted nodes/edges, bounded flag |
| Memory | Graph + history → stable_hash |
| Replay | Graph hash, global fingerprint, DOM hash, browser identity |
| Reconstruction | Deterministic runtime_id from IR |

---

## 3. Deterministic normalization

### String

1. Unicode **NFKC**
2. `\r\n` and `\r` → `\n`
3. Trailing whitespace stripped

### Objects

- Keys sorted lexicographically at every object level
- **Volatile keys removed:** `timestamp`, `created_at`, `updated_at`, `nonce`, `request_id`, `csrf`, `generated_at`, `runtime_id`, `random`, `uuid`
- Arrays: index keys `0`, `1`, … when serialized as objects (parity rule)

### DOM stabilization

- UUID → `uuid-stabilized`
- ISO timestamps → `timestamp-stabilized`
- Strip React/Vue/Angular noise attrs, `nonce`, script bodies → `<script>stabilized</script>`
- Collapse whitespace

### Network events

Sort by `method|url`.

---

## 4. Runtime graph (canonical)

```json
{
  "nodes": [
    { "id": "node:<kind>:<idx>", "type": "<kind>", "payload": {} }
  ],
  "edges": [
    { "source": "node:…:0", "target": "node:…:1", "type": "runtime_link" }
  ],
  "bounded": true
}
```

- Nodes sorted by `id|type|name`
- Edges sorted by `source|target|type`
- `graphFingerprint` = SHA-256(`stableSerialize(normalized graph)`)

---

## 5. Replay equivalence

`validateReplayEquivalence(original, replayed)` MUST check:

| Check | Rule |
|-------|------|
| `graph_hash` | Fingerprint of normalized nodes+edges |
| `global_fingerprint` | Pipeline + graph digest |
| `browser_identity` | `browser_ir.runtime_identity` equality |
| `dom_stabilized_hash` | When DOM present, `computeStableDomHash` match |
| `semantic_fingerprint` | Combined graph + global fingerprint |

Returns: `{ equivalent: bool, checks: [...], bounded: true }`.

---

## 6. Runtime memory

```json
{
  "memory": { "graph": {}, "runtime_history": [] },
  "stable_hash": "<sha256>",
  "bounded": true
}
```

- `stableMemoryHash` = SHA-256(`stableSerialize({ graph, history_len })`)
- `queryRuntimeMemory(mem, key)` returns keyed slice
- `mergeRuntimeMemories` unions graphs and history

---

## 7. Reconstruction

`reconstructRuntime({ extraction })` returns:

```json
{
  "runtime_id": "<first 16 hex of hash(graph)>",
  "graph": {},
  "bounded": true,
  "reconstructed": true
}
```

---

## 8. Kaalka parity (cross-language)

```text
normalizeRuntimeValue → stableSerialize → UTF-8
  → deriveKaalkaTimeKey(key)   // SHA-256 probe, HH:MM:SS round-trip
  → kaalka@5.0.0 _proc(bytes, encrypt)
  → base64 ciphertext
```

**Hash:** `SHA-256(stableSerialize(value))` as lowercase hex.

**Registry only:** `kaalka@5.0.0` — no local forks.

**Vectors:** `validation/parity/javascript_vectors.json` (reference), `python_vectors.json`, `dart_vectors.json`.

---

## 9. Required public API (all languages)

| Capability | Python | JavaScript | Dart |
|------------|----------|------------|------|
| Extract web | `extract_web` | `extractWeb` | `extractWeb` |
| Pipeline | `run_canonical_pipeline` | `runCanonicalPipeline` | `runCanonicalPipeline` |
| Encrypt | `encrypt_value` | `encryptValue` | `encryptValue` |
| Decrypt | `decrypt_value` | `decryptValue` | `decryptValue` |
| Hash | `compute_deterministic_hash` | `computeDeterministicHash` | `computeDeterministicHash` |
| Replay | `validate_replay_equivalence` | `validateReplayEquivalence` | `validateReplayEquivalence` |
| Normalize | `normalize_runtime_value` | `normalizeRuntimeValue` | `normalizeRuntimeValue` |
| Graph | `build_runtime_graph` | `buildRuntimeGraph` | `buildRuntimeGraph` |
| Reconstruct | `reconstruct_runtime` | `reconstructRuntime` | `reconstructRuntime` |
| Memory query | `query_runtime_memory` | `queryRuntimeMemory` | `queryRuntimeMemory` |

---

## 10. Validation gates (per branch)

| Gate | Command |
|------|---------|
| Parity | See `validation/parity/` |
| Replay | See `validation/replay/` |
| Ecosystem | See `validation/validate_ecosystem.*` |

All implementations MUST pass **11/11** crypto parity vectors before claiming cross-language lock.
