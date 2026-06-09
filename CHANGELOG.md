# Changelog

## [2.0.0] — 2026-06-09 — Dart native release

### Added

- Native Dart runtime cognition infrastructure for humans and AI agents
- Kaalka v5 parity pipeline (`kaalka@5.0.0` from pub.dev)
- Cross-language validation (11/11 JavaScript reference vectors)
- Browser HTTP extraction, replay equivalence, runtime memory, reconstruction
- GitHub Actions CI on `dart` branch

### Quality

- Comprehensive unit-test suite: **290 tests** across crypto, determinism,
  graph, replay, memory, reconstruction, kernel, browser, and connector
  subsystems
- **99.59% line coverage** (`dart test --coverage`); the only uncovered line is
  the Node-subprocess NFKC fallback in `normalization.dart`, which is
  unreachable when Node.js is on `PATH`
- `dart analyze` clean (zero issues) under strict-casts + strict-inference
- `dart format` clean across the package
- `dart pub publish --dry-run` clean (no packaging warnings)

### Security

- No auth bypass, CAPTCHA defeat, or credential cracking
