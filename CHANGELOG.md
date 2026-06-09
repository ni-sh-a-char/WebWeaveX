# Changelog

## [2.0.0] — 2026-06-09 — Dart native release

### Added

- Native Dart runtime cognition infrastructure for humans and AI agents
- Kaalka v5 parity pipeline (`kaalka@5.0.0` from pub.dev)
- Cross-language validation (11/11 JavaScript reference vectors)
- Browser HTTP extraction, replay equivalence, runtime memory, reconstruction
- GitHub Actions CI on `dart` branch

### Runtime parity

- Ported **12 runtime-cognition families** to native Dart with **proven
  cross-language hash parity** — Dart output hashes byte-identically to Python's
  `compute_deterministic_hash` (`computeDeterministicHash(dartOut) == h(pyOut)`),
  save/load proven by temp-file roundtrip: `causality`, `semantic`,
  `synchronization`, `evolution_runtime`, `workflows`, `execution`,
  `memory-runtime`, `reconstruction-runtime`, `connectors/streaming/interaction`,
  `query/reasoning`, `persistence/crypto-session/identity/adaptive/distributed/
  session/auth`, `kernel/contracts/unified-IR` — **+72 public APIs**.
- Public-API parity vs Python `__all__`: **88/128 Complete**, 23 Partial,
  17 Deferred (OS/desktop/Electron/DevTools — documented), **0 Missing**. See
  `PUBLIC_API_MATRIX.md`, `DART_PARITY_AUDIT.md`, `DART_RELEASE_GAP_REPORT.md`.
- ~145 parity-proof vectors in `validation/parity/*_api_vectors.json`;
  assertions in `test/parity/*_parity_test.dart`. Honestly bounded (not faked):
  `compile_document`/`compile_repository` (need NLP/AST), `run_canonical_pipeline`
  (deterministic core only), and document/repository sub-paths of the query
  family — all classified Partial in the matrix.

### Quality

- Comprehensive unit-test suite: **779 tests** across all subsystems and the
  12 newly-ported runtime families
- **97.23% line coverage** (`dart test --coverage`); the only sub-90% file is
  `normalization.dart` (Node-subprocess NFKC fallback, unreachable when Node is
  on `PATH`)
- `dart analyze` clean (zero issues) under strict-casts + strict-inference
- `dart format` clean across the package
- `dart pub publish --dry-run` clean (no packaging warnings)

### Security

- No auth bypass, CAPTCHA defeat, or credential cracking
