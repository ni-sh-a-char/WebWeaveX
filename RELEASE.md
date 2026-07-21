# Release Process

## Prerequisites

1. All 133 tests passing
2. Cross-language parity verified
3. Documentation complete
4. CHANGELOG updated

## Steps

1. Update version in `build.gradle.kts`
2. Update CHANGELOG.md
3. Run `gradle clean test`
4. Commit: `git commit -m "release: v3.0.0"`
5. Tag: `git tag v3.0.0`
6. Push: `git push origin kotlin --tags`
7. Build artifact: `gradle build`
8. Verify: `ls -la build/libs/`
