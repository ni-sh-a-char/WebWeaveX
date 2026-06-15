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
> byte-exact against canonical Python 2.1.0. Higher layers (kernel, graph, IR,
> query, extraction, vision, …) are tracked in
> [`JAVA_PARITY_MATRIX.md`](JAVA_PARITY_MATRIX.md) and built in subsequent
> sessions. No stubs or placeholders are shipped — only implemented, tested code.

## What is implemented and parity-proven today

| Package | Contents |
| --- | --- |
| `io.webweavex.determinism` | `Normalization` (NFKC + CRLF + trailing-whitespace strip, code-point key ordering, volatile-key stripping, numeric canonicalization), `PyFloat` (Python `repr(float)`), `CanonicalJson` (compact sorted-key `ensure_ascii=False` encoder), `StableSerialize` |
| `io.webweavex.crypto` | `Hashing` (`sha256(utf8(stableSerialize))`), `KaalkaV5Proc` (Kaalka v5 byte cipher), `TimeKey` (time-key derivation), `Kaalka` (`computeKaalkaHash`, `encryptValue`, `decryptValue`, envelopes) |

Public APIs from `PARITY_MANIFEST.json` now live: `compute_kaalka_hash`,
`encrypt_value`, `decrypt_value`.

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

**98 tests pass** (80 cross-language byte-exact assertions + 18 unit). Because
Python ≡ JavaScript ≡ Dart is already certified (70k+ byte-identical
comparisons), proving Java ≡ Python proves Java ≡ JS ≡ Dart for these primitives.

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

Coordinates: `io.webweavex:webweavex:2.1.0`.

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
