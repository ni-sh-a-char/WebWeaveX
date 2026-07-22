# Changelog

All notable changes

## [3.0.0] — 2026-07-12 — Reference implementation certification

### Changed
- Fixed broken test suite (was 0 passing due to missing benchmarks module).
- Removed 46 stale/duplicate files across CERT-01 through CERT-02.
- Added 53 certification tests (determinism, reliability, platform).
- Consolidated serialization to single canonical implementation.
- Updated requirements.txt to sync with pyproject.toml.
- Reference implementation certified as canonical platform specification.

### Fixed
- Schema test paths corrected (contracts/schemas/ -> core/schemas/contracts/).
- Example version references updated (v2.0.0 -> v3.0.0).
- README coverage badge corrected to match actual (88%+).
 to WebWeaveX are documented here.

## [2.1.0] — 2026-06-12 — Synchronized cross-language release

### Changed
- Synchronized version **2.1.0** across PyPI (Python), npm (JavaScript), and pub.dev (Dart).
- Standardized README structure across all three implementations (equivalent sections:
  Core Capabilities, Common Workflows, Supported Platforms, Versioning).
- Consolidated release staging into the canonical `python` / `javascript` / `dart` branches and
  removed the `release/*` staging branches.
- Re-ran cross-language parity, determinism, and publication validation against this version.

### Notes
- **No public API behavior changes.** The cross-language deterministic contract and hashes are
  unchanged from 2.0.x; the internal engine version (`v1_phase_14`) is intentionally unchanged.
- Shared docs (`ARCHITECTURE.md`, `CERTIFICATION.md`, `AI_AGENT_GUIDE.md`, `API_REFERENCE.md`,
  `LICENSE`) are byte-identical across all three implementations.

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
