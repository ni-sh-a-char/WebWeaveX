# CI_VALIDATION_REPORT.md

CI for the `dart` branch is defined in `.github/workflows/dart.yml` and triggers on push/PR to `dart`. (`ci.yml` is the Python product's workflow for `main`/`master` and is intentionally untouched.)

## `dart.yml` job: `validate` (ubuntu-latest)

| Step | Command | Gate |
|------|---------|------|
| Setup | `dart-lang/setup-dart@v1` (stable) + `actions/setup-node@v4` (20) | Node present for NFKC parity |
| Install | `dart pub get` | deps resolve |
| Format | `dart format --set-exit-if-changed .` | fails on any unformatted file |
| Analyze | `dart analyze` | fails on any issue (strict-casts + strict-inference) |
| Test | `dart test` | all tests must pass |
| Coverage | `dart test --coverage` → `format_coverage` → awk gate | **fails if line coverage < 90%** |
| Parity | `dart run validation/validate_parity.dart` | cross-language vectors must match |
| Publish | `dart pub publish --dry-run` | package must be publishable |

## Local reproduction (matches CI, measured in canonical repo)

| Gate | Local result |
|------|--------------|
| `dart format --set-exit-if-changed .` | clean |
| `dart analyze` | No issues found! |
| `dart test` | 779 passing |
| Coverage ≥90% | 97.2% (see `COVERAGE_REPORT.md`) |
| `dart run validation/validate_parity.dart` | parity vectors match |
| `dart pub publish --dry-run` | 0 warnings (benign version hint only) |

All CI gates pass locally against the canonical `dart` checkout; the workflow runs the identical commands on push/PR.
