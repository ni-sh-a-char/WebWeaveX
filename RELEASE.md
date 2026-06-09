# Release Process (Dart / pub.dev)

WebWeaveX Dart releases are version-aligned with the Python (PyPI) and JavaScript (npm)
implementations. The current line is **2.0.1**.

## Pre-release checklist

Run from a clean working tree on the `dart` branch:

```bash
dart format --set-exit-if-changed .
dart analyze
dart test                                     # 779+ passing, 0 failing
dart test --coverage=coverage && \
  dart pub global run coverage:format_coverage --lcov --in=coverage \
  --out=coverage/lcov.info --report-on=lib --packages=.dart_tool/package_config.json
dart run validation/validate_parity.dart      # crossLangMatch: true
dart pub publish --dry-run                     # 0 warnings
```

All gates must be green. Coverage must be ≥ 90%.

## Version bump

1. Update `version:` in `pubspec.yaml` (keep aligned with Python/JS).
2. Update `CHANGELOG.md` with the new version and notable changes.
3. Regenerate validation reports (`FINAL_STATE_OF_DART_BRANCH.md`, parity matrix).
4. Commit with a `release(dart): version X.Y.Z` message.

## Publishing

```bash
dart pub publish
```

Requires pub.dev maintainer credentials for the `webweavex` package. The dry-run reports a
benign hint while the live pub.dev version trails the cross-language-aligned version.

## Post-release

- Tag the release commit.
- Verify the package page on pub.dev renders the README and example correctly.
- Open the next development cycle per [ROADMAP.md](ROADMAP.md).
