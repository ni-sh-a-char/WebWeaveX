# OSS_VALIDATION_REPORT.md

> Measured 2026-06-10 by `Test-Path` / `wc -c` on the working tree and `git ls-tree`
> against `origin/javascript` for cross-branch governance comparison.

## Core OSS files (all present on `dart`)

| File | Status | Bytes |
|------|--------|------:|
| LICENSE (Apache-2.0) | ✅ present | 660 |
| NOTICE | ✅ present | 129 |
| AUTHORS | ✅ present | 14 |
| CHANGELOG.md | ✅ present | 2154 |
| CONTRIBUTING.md | ✅ present | 1687 |
| SECURITY.md | ✅ present | 695 |
| CODE_OF_CONDUCT.md | ✅ present | 186 |
| ROADMAP.md | ✅ present | 860 |
| CITATION.cff | ✅ present | 232 |

All nine mission-required OSS files exist. The package also ships `analysis_options.yaml`,
`.pubignore`, `.gitignore`, and a `docs/` tree.

## Governance files present on `javascript` but absent on `dart`

| File | On JS | On Dart | Recommendation |
|------|:-----:|:-------:|----------------|
| CODEOWNERS | ✓ | ❌ | Add — routes review ownership |
| GOVERNANCE.md | ✓ | ❌ | Add — decision/maintainer model |
| MAINTAINERS.md | ✓ | ❌ | Add — named maintainers |
| RELEASE.md | ✓ | ❌ | Add — Dart/pub.dev release process |
| SUPPORT.md | ✓ | ❌ | Add — support channels |

## Content-quality observations

- `CODE_OF_CONDUCT.md` (186 bytes) and `AUTHORS` (14 bytes) are stubs — functional but thin
  compared to the Contributor Covenant used on the sibling branches.
- `CONTRIBUTING.md` is present but does not yet document the Dart-specific gate sequence
  (`dart format` / `analyze` / `test` / coverage / `pub publish --dry-run`).

## Verdict

OSS gate **PASS** on the mandatory set (9/9 present). For full governance parity with the
JavaScript branch, add the **5 missing governance files** (CODEOWNERS, GOVERNANCE, MAINTAINERS,
RELEASE, SUPPORT) and expand the CODE_OF_CONDUCT stub to the full Contributor Covenant. All of
this is fully achievable with no platform constraints.
