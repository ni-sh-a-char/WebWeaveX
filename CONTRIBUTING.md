# Contributing to WebWeaveX (Dart)

Thank you for helping improve deterministic runtime cognition infrastructure. This is the
**Dart** (pub.dev) implementation; it is parity-aligned with the canonical Python (PyPI) and
JavaScript (npm) branches.

## Setup

```bash
git clone https://github.com/ni-sh-a-char/WebWeaveX.git
cd WebWeaveX
git checkout dart
dart pub get
```

Requires Dart SDK `>=3.3.0 <4.0.0` (developed on 3.8.2).

## Before you open a PR

Run the full gate sequence — all must pass:

```bash
dart format --set-exit-if-changed .
dart analyze
dart test
dart run validation/validate_parity.dart      # crossLangMatch: true
dart pub publish --dry-run
```

Coverage must remain **≥ 90%** (CI enforces this in `.github/workflows/dart.yml`):

```bash
dart test --coverage=coverage
dart pub global run coverage:format_coverage --lcov --in=coverage \
  --out=coverage/lcov.info --report-on=lib --packages=.dart_tool/package_config.json
```

## Design rules

1. **Canonical pipeline only** — new runtime behavior integrates with `runCanonicalPipeline()`
   or an existing phase orchestrator; no parallel mega-orchestrators.
2. **Determinism** — no `Random`, no UUIDs, no time-based IDs in persisted or hashed structures.
   `List.sort` must use an index-tiebreak comparator to match Python's stable `sorted`.
3. **Kaalka persistence** — operational checkpoints use `encryptValue` / session wrappers; no
   plaintext runtime stores.
4. **Replay-safe** — graph normalization and fingerprints must remain stable for equivalent inputs.
5. **Bounded output** — public functions return maps with `bounded: true` where applicable.
6. **No import-time side effects** — importing the package must not launch network jobs.

## Cross-language parity is proven, never assumed

Any new or changed public API must ship with:

- a hash-parity vector under `validation/parity/*_api_vectors.json`, and
- a test in `test/parity/` asserting
  `computeDeterministicHash(dartOutput) == <Python/JS reference hash>`.

The reference hash is generated from the Python branch
(`compute_deterministic_hash`, byte-identical to Dart's `computeDeterministicHash`).

## Code style

- Match surrounding modules: explicit collection type arguments (required under
  strict-casts / strict-inference), minimal comments, `library;` directives.
- Prefer extending existing engines over new top-level shim files.
- Tests assert real behavior, not implementation trivia. Put coverage tests in `test/engines/`
  (note: `test/coverage/` is gitignored).

## Pull requests

Use `.github/PULL_REQUEST_TEMPLATE.md`. Keep commits logically grouped with professional messages.

## Questions

Open a [GitHub issue](https://github.com/ni-sh-a-char/WebWeaveX/issues) or see [SUPPORT.md](SUPPORT.md).
