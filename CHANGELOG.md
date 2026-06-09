# Changelog

## [2.0.0] — 2026-06-09 — Dart native release

### Added

- Native Dart runtime cognition infrastructure for humans and AI agents
- Kaalka v5 parity pipeline (`kaalka@5.0.0` from pub.dev)
- Cross-language validation (11/11 JavaScript reference vectors)
- Browser HTTP extraction, replay equivalence, runtime memory, reconstruction
- GitHub Actions CI on `dart` branch

### Runtime parity

- Ported 6 runtime-cognition families to native Dart with **proven
  cross-language hash parity** (Dart output hashes byte-identically to Python's
  `compute_deterministic_hash`): `causality`, `semantic`, `synchronization`,
  `evolution_runtime`, `workflows`, `execution` — **+35 public APIs**.
- Public-API parity vs Python `__all__`: **51/128 Complete**, 15 Partial,
  17 Deferred (OS/desktop/Electron/DevTools — documented), 45 Missing. See
  `PUBLIC_API_MATRIX.md`, `DART_PARITY_AUDIT.md`, `DART_RELEASE_GAP_REPORT.md`.
- Parity proof vectors: `validation/parity/*_api_vectors.json`;
  assertions in `test/parity/*_parity_test.dart`.

### Quality

- Comprehensive unit-test suite: **551 tests** across crypto, determinism,
  graph, replay, memory, reconstruction, kernel, browser, connectors, and the
  6 newly-ported runtime families
- **96.93% line coverage** (`dart test --coverage`); the two sub-90% files are
  `normalization.dart` (Node-subprocess NFKC fallback, unreachable when Node is
  on `PATH`) and `semantic_engines.dart` (non-empty-HTML UI/table path,
  documented gap — no BeautifulSoup equivalent bundled)
- `dart analyze` clean (zero issues) under strict-casts + strict-inference
- `dart format` clean across the package
- `dart pub publish --dry-run` clean (no packaging warnings)

### Security

- No auth bypass, CAPTCHA defeat, or credential cracking
