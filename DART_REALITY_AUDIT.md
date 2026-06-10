# DART_REALITY_AUDIT.md

> Phase 1 — measured from source on 2026-06-10 at HEAD `3bd9cf7` (+ uncommitted Wave-4 work).
> Every number is produced by an executed measurement script over the live tree, never estimated.

## Source structure (measured from `lib/`)

| Metric | Value | How measured |
|--------|------:|--------------|
| Dart source files (`lib/**/*.dart`) | 148 | filesystem walk |
| Public top-level functions | 376 | regex over typed-return declarations |
| Public classes | 7 | `class` declarations |
| Barrel `export` lines (`lib/webweavex.dart`) | 55 | grep |
| Instrumented lib files (coverage) | 135 | LCOV `SF:` records |

## Tests (measured by `dart test`)

| Metric | Value |
|--------|------:|
| Tests executed | **802** (all passing, 0 failing) |
| Test files | 35 |
| Parity vector files (`validation/parity/*.json`) | 17 |
| Total parity vector cases | 223 |

## Coverage (fresh LCOV)

| Metric | Value |
|--------|------:|
| Line coverage | **97.26%** (6394/6574) |
| Files below 90% | 1 (`normalization.dart`, 85.71% — unreachable Node NFKC fallback line) |

## Static analysis & format

| Gate | Result |
|------|--------|
| `dart format --set-exit-if-changed .` | clean |
| `dart analyze` (strict-casts + strict-inference) | No issues found |

## Public API surface vs the canonical Python contract

| Implementation | Canonical APIs present | Source measured |
|----------------|-----------------------:|-----------------|
| Python (`webweavex.__all__`) | 126 (+`version`,`__version__`) | `origin/python:webweavex/__init__.py` |
| JavaScript | 126 / 126 | `origin/javascript:src/index.ts` + `publicApi.ts` + `connectors/index.ts` |
| Dart (native symbol) | 96 / 126 | `lib/**` symbols mapped snake→camel |

## API parity classification (regenerated `tools/dart_parity_audit.py`)

| Status | Count |
|--------|------:|
| ✅ Complete | 79 |
| 🟡 Partial | 34 |
| ⚪ Deferred | 15 |
| ❌ Missing | 0 |

## Version alignment (measured)

| Implementation | File | Version |
|----------------|------|---------|
| Python | `pyproject.toml` | 2.0.1 |
| JavaScript | `package.json` | 2.0.1 |
| Dart | `pubspec.yaml` | 2.0.1 |

## Governance & OSS files present

LICENSE, NOTICE, AUTHORS, CHANGELOG.md, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md,
ROADMAP.md, CITATION.cff, GOVERNANCE.md, MAINTAINERS.md, CODEOWNERS, RELEASE.md, SUPPORT.md.

## Workflows present

`.github/workflows/ci.yml`, `.github/workflows/dart.yml` (format, analyze, test, coverage gate).

## Verdict

The branch is internally consistent and measured: 148 source files, 802 passing tests, 97.26%
coverage, 79/34/15/0 parity, version-aligned 2.0.1, all gates green. Reality matches the
classification — see `FINAL_TRUE_PARITY_REPORT.md` for the proof-coverage and honesty analysis.
