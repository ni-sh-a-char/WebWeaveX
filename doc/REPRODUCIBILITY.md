# Reproducibility Index

## Environment

| Component | Version |
|-----------|---------|
| Dart SDK | >=3.3.0 <4.0.0 |
| OS | Linux / macOS / Windows |
| Package | webweavex 3.0.0 |
| Kaalka | 5.0.0 |

## Tests

```bash
dart test
```
Expected: 537/537 pass

## Determinism (1000 iterations)

```bash
dart test test/determinism/determinism_stress_test.dart
```
Expected: 7/7 pass — bit-identical output across 1000 iterations for:
- stableSerialize
- normalizeRuntimeValue
- graphFingerprint
- computeRuntimePipelineFingerprint
- validateReplayEquivalence
- computeGlobalRuntimeFingerprint
- Key ordering

## Replay Validation

```bash
dart test test/cert02_behavioral_test.dart
```
Expected: 9/9 pass — replay, memory, knowledge graph validation

## Parity Validation

```bash
dart run validation/validate_parity.dart
```
Expected: crossLangMatch: true

## Coverage

```bash
dart test --coverage=coverage
dart pub global run coverage:format_coverage --lcov --in=coverage --out=coverage/lcov.info --report-on=lib
```
