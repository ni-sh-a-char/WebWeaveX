# Cross-Language Verifier

Automated parity harness proving `Python == JavaScript == Dart` byte-identity
for the WebWeaveX deterministic core: stable serialization, canonical JSON
(`dumps_deterministic`), SHA-256 hashing, Kaalka v5 encryption (Base64),
encryption roundtrip, and the Kaalka v1 hex fingerprint.

## Layout

| File | Purpose |
| --- | --- |
| `generate_vectors.py` | Deterministic generator: 1100 torture vectors (multilingual Unicode incl. Hindi/Arabic/CJK/Korean/emoji/astral/RTL/bidi/combining, float matrix, key-ordering sets, nested structures, volatile keys, large payloads, 900+ seeded random structures). Seeded — no time or machine state. |
| `run_python.py` | Python runner (set `PYTHONPATH` to a materialized `python` branch). |
| `run_js.mjs` | JavaScript runner (copy into a materialized `javascript` branch, run with `npx tsx`). |
| `run_dart.dart` | Dart runner (run from this repo root: `dart run cross_language_verifier/run_dart.dart cross_language_verifier/vectors.json out.json`). |
| `compare.py` | Comparator: per-language determinism (3 runs) + cross-language byte equality per field; emits `parity_report.json`, `failure_vectors.json`, `certification_report.json`. Exit 0 only on full PASS. |
| `kaalka_parity_matrix.json` | Documented Kaalka call paths, pre/post-processing, and the serialization contract per language. |

## Protocol

1. `python generate_vectors.py`
2. Run each language runner **3 times** (`out_<lang>_{1,2,3}.json`).
3. `python compare.py` — verdict PASS requires every field byte-identical in
   all three languages and all three runs identical per language.

## Certified result (2026-06-11)

- 1100 vectors x 6 fields + time key = **6601/6601 byte-identical**
- 3/3 runs identical per language; all encryption roundtrips pass
- Dart verified standalone: byte-identical output with Node.js removed from PATH

## Input-domain contract

- integers: `|n| <= 2^53`
- floats: IEEE-754 doubles; integral floats `< 2^63` canonicalize to integers;
  non-finite values -> `null` (stable path) / `0` (fingerprint path);
  fractional floats render as Python `repr` (shortest round-trip digits,
  positional for decimal exponent in `[-4, 15]`, else `e±NN`)
- strings: Unicode scalar sequences (no lone surrogates); NFKC applies to
  top-level strings, NFC on the fingerprint path
- dict keys: sorted by Unicode code point (Python `sorted` semantics)
