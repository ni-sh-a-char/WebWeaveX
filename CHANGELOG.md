# Changelog

All notable changes to WebWeaveX are documented here.

## [2.0.0] — 2026-05-21 — Official open-source release

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
- Test suite consolidated — **671 tests passing**
- `pyproject.toml` production extras: `[browser]`, `[full]`, classifiers, keywords

### Removed
- Internal audit reports, phase dumps, and `scripts/**` JSON matrix artifacts
- Archive directories (`docs/archive`, `tests/archive`)

### Security
- Kaalka-mandatory persistence for operational checkpoints
- Bounded execution sandbox — no `eval` / `exec` in production paths

## [1.1.1] — Production finalization (pre-release)

Kernel, unified IR, AST cognition, WWX language, and publication hardening.
