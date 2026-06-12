# pub.dev Release Checklist — WebWeaveX 2.1.0 (Dart)

> Prepared, not published. Publication is a maintainer-gated step.

**Branch:** `dart` · **Package:** `webweavex` · **Version:** `2.1.0`
**Certified commit:** `b223457447529098fd7dfd4772a2679e44c5a966`

## Pre-flight (already verified this release)

- [x] `pubspec.yaml` version = `2.1.0`; `lib/webweavex.dart` `const version` = `2.1.0`
- [x] `dart pub get` resolves
- [x] `dart analyze` → No issues found!
- [x] `dart test` → 1583 passed
- [x] `dart pub publish --dry-run` → 0 warnings (1 benign version-increment hint)
- [x] `CHANGELOG.md` has a `[2.1.0]` entry

> Note: pub.dev currently shows `0.1.1` for this package, so the dry-run emits a
> non-blocking hint about the version jump. `2.1.0` is intentional — it is the
> synchronized cross-language version shared with PyPI and npm.

## Build & verify

```bash
git clone --branch dart --single-branch https://github.com/ni-sh-a-char/WebWeaveX.git wwx-dart
cd wwx-dart
dart pub get
dart analyze
dart test
dart pub publish --dry-run
```

## Publish (maintainer only)

```bash
dart pub login        # opens browser OAuth for the publisher account
dart pub publish      # confirm the file list and version prompt
```

## Post-publish

- [ ] `dart pub global activate webweavex 2.1.0` or add `webweavex: ^2.1.0` in a sample app; verify import
- [ ] Confirm version on https://pub.dev/packages/webweavex
- [ ] Tag the release: `git tag v2.1.0 && git push origin v2.1.0`
- [ ] Create GitHub Release notes from the `[2.1.0]` CHANGELOG section
