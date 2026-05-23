# Changelog

All notable changes to WebWeaveX are documented here.

## [2.0.0] — 2026-05-23 — npm (JavaScript) public release

### Added
- Deterministic runtime cognition infrastructure for **humans and AI agents**
- Browser-native extraction (`extractWeb`), Playwright rendering, DOM stabilization
- Authenticated runtime continuation, replay equivalence, reconstruction, runtime memory
- Cross-language parity with Python via `kaalka@5.0.0` + canonical normalization pipeline
- Production validation gates (`validate:parity`, `validate:production`)

### Changed
- **Kaalka v5** from npm registry only (`kaalka@5.0.0`); byte `_proc` + base64 ciphertext
- ESM/CJS dual publish via `tsup`; `sideEffects: false`

### Security
- No auth bypass, CAPTCHA defeat, or credential cracking — authorized session material only

## [2.0.0] — 2026-05-21 — Ecosystem open-source release

### Added
- Universal **Runtime Kernel** (`core/kernel/`) — single orchestration substrate
- **Unified runtime IR** — merged cognition across all phases
- **Repository AST cognition** — Python AST + multi-language structural parsers
- **WWX runtime language** — declarative extraction / sync / execute plans
- Federated memory, execution sandbox, and reconstruction fabrics (Phases W–Y)
- Professional documentation under `docs/`
- Viral open-source README and Apache 2.0 release structure

### Changed
- Version bumped to **2.0.0** across package and public API
- Repository sanitized — removed audit markdown spam and 450+ generated JSON dumps
- Test suite consolidated — **760+ tests passing**, scoped coverage **≥ 90%**
- `pyproject.toml` production extras: `[browser]`, `[full]`, classifiers, keywords

### Removed
- Internal audit reports, phase dumps, and stale generated JSON matrix artifacts
- Legacy V7 orchestrators, dead modules, and duplicate validation markdown at repository root

### Security
- Kaalka-mandatory persistence for operational checkpoints
- Bounded execution sandbox — no `eval` / `exec` in production paths

## [1.1.1] — Production finalization (pre-release)

Kernel, unified IR, AST cognition, WWX language, and publication hardening.
