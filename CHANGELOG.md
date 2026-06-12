# Changelog

All notable changes to WebWeaveX are documented here.

## [2.1.0] — 2026-06-12 — Synchronized cross-language release

### Changed
- Synchronized version **2.1.0** across npm (JavaScript), PyPI (Python), and pub.dev (Dart).
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

## [2.0.1] — 2026-06-08 — convergence & independent-product certification

### Fixed
- **Python product import chain** — `core.determinism` now re-exports
  `compute_global_runtime_fingerprint` (PEP 562 lazy `__getattr__`, cycle-safe),
  repairing `import webweavex` for the pip product.

### Changed
- **Public API surface** — the JavaScript package now exposes a
  specification-conforming surface mirroring the Python `__all__` (128/128
  names); `buildRuntimeGraph`/`queryRuntimeGraph` resolve to the spec
  list-of-IRs engines.
- Generated runtime regenerated end-to-end; full `tsc` strict typing
  (`@ts-nocheck = 0`).

### Certification (measured from fresh execution)
- Implementation equality matrix **1724/1724 EQUAL**; API parity **128/128**.
- JavaScript: **399 tests**, coverage 99.17 / 99.65 / 95.45 / 99.17.
- Python: **772 tests**, `twine check` passed, installs in a clean venv.
- Determinism **100/100, 0 drift**; real-world **1200 URLs, 100% match, 0% drift**.
- Runtime independence: JS Python-free, Python Node-free.
- `specification/` is the sole authority; both products conform.

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
