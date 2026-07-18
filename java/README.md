# WebWeaveX — Java

Deterministic runtime cognition infrastructure. Java implementation targeting
**byte-exact cross-language parity** with the Python (canonical), JavaScript, and
Dart runtimes:

```
Python  =  Java  =  JavaScript  =  Dart
```

> **Status: foundation slice (in progress).** This branch builds the runtime
> **foundation-first**. The deterministic + cryptographic bedrock — through which
> every other subsystem hashes and serializes — is implemented and verified
> byte-exact against canonical Python 3.0.0. Higher layers (kernel, graph, IR,
> query, extraction, vision, …) are tracked in
> [`JAVA_PARITY_MATRIX.md`](JAVA_PARITY_MATRIX.md) and built in subsequent
> sessions. No stubs or placeholders are shipped — only implemented, tested code.

## What is implemented and parity-proven today

| Package | Contents |
| --- | --- |
| `io.webweavex.determinism` | `Normalization`, `PyFloat` (Python `repr(float)`), `CanonicalJson`, `StableSerialize`, `PyJson` (faithful `json.dumps`), `Py` (Python `str`/truthiness), `GlobalRuntimeFingerprint` |
| `io.webweavex.crypto` | `Hashing` (`sha256(utf8(stableSerialize))`), `KaalkaV5Proc` (Kaalka v5 byte cipher), `TimeKey`, `Kaalka` (`computeKaalkaHash`, `encryptValue`, `decryptValue`, envelopes) |
| `io.webweavex.kernel` | `UniversalInput` (canonical ingress descriptor, `to_dict` parity) |
| `io.webweavex.graph` | `RuntimeGraph` (`buildParityRuntimeGraph`, `normalizeRuntimeGraph`, `normalizeContract`, `graphFingerprint`) |
| `io.webweavex.ir` | `UnifiedRuntimeIr` (`compile`, `toGraph`), `MultimodalIr` |
| `io.webweavex.persistence` | `FingerprintHex` (Kaalka v1 `hex_fingerprint` + NFC `dumps_deterministic`) |
| `io.webweavex.replay` | `ReplayEquivalence` (`validate_replay_equivalence`) |

Public APIs from `PARITY_MANIFEST.json` now live (9): `compute_kaalka_hash`,
`encrypt_value`, `decrypt_value`, `UniversalInput`, `build_runtime_graph`,
`compile_unified_runtime_ir`, `compute_global_runtime_fingerprint`,
`fingerprint`, `validate_replay_equivalence`.

> **Conform-to-Python rule:** session-2 APIs are ported directly from the Python
> `core/` canon (e.g. `core.determinism.runtime_graph_parity`,
> `core.ir.unified_runtime_ir`, `core.crypto.kaalka_engine`), not from the Dart
> wrappers — some Dart public symbols diverge from Python. Every output is
> verified byte-exact against Python via `golden_vectors_s2.json`.

## Parity proof

`io.webweavex.parity.CrossLanguageParityTest` loads
`src/test/resources/parity/golden_vectors.json` — fixtures generated from a
materialized canonical Python branch by `tools/gen_java_parity_vectors.py` — and
asserts Java is byte-identical for:

- canonical `stable_serialize` output (objects, arrays, scalars, nested)
- SHA-256 content hashes
- NFKC + CRLF + trailing-whitespace normalization
- code-point key ordering and volatile-key stripping
- Python `repr(float)` (positional / scientific thresholds, integral collapse)
- Kaalka time-key derivation, base64 ciphertext, and decrypt round-trips

**132 tests pass** (102 cross-language byte-exact assertions + 30 unit), across
both `CrossLanguageParityTest` (determinism/crypto) and
`CrossLanguageParityS2Test` (kernel/graph/ir/persistence/fingerprint/replay).
Because Python ≡ JavaScript ≡ Dart is already certified (70k+ byte-identical
comparisons), proving Java ≡ Python proves Java ≡ JS ≡ Dart for these APIs.

## Build

```bash
cd java
mvn clean verify        # compile, test, coverage, jar + sources + javadoc
mvn -Prelease verify    # additionally GPG-signs artifacts for Maven Central
```

- Java 17+ (built and tested on JDK 21)
- The deterministic core depends on the **JDK alone** (`java.text.Normalizer`,
  `MessageDigest`, `Base64`) — no third-party library can perturb canonical bytes.
  Jackson is a **test-only** dependency used to load golden vectors.

Coordinates: `io.webweavex:webweavex:3.0.0`.

## Regenerating golden vectors

```bash
# from a materialized Python-branch checkout (so `core` is importable)
python tools/gen_java_parity_vectors.py java/src/test/resources/parity/golden_vectors.json
```

## Coverage

JaCoCo: **~93% instruction**. The uncovered remainder is unreachable defensive
code faithfully mirrored from the canonical runtimes — the JDK-guaranteed
`NoSuchAlgorithmException` catches for SHA-256, the Kaalka time-key fallback
(a pure modular cipher always round-trips, so the first candidate always
returns), and float-format safety branches. These are intentionally retained as
1:1 parity mirrors rather than removed to inflate the metric.

