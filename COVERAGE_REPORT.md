# COVERAGE_REPORT.md

Measured by `dart test --coverage=coverage` + `package:coverage` `format_coverage` over `lib/` in the canonical repo (`dart` branch). Real coverage — no exclusions, no dead-code tricks.

## Total

**97.23% line coverage — 6280 / 6459 lines.** Target 90% — **met with margin.**

```bash
dart test --coverage=coverage
dart pub global run coverage:format_coverage --lcov --in=coverage \
  --out=coverage/lcov.info --report-on=lib --packages=.dart_tool/package_config.json
```

## Per top-level package

| Package | Coverage | Lines |
|---------|---------:|-------|
| browser | 100.00% | 146/146 |
| distributed | 100.00% | 12/12 |
| graph | 100.00% | 87/87 |
| kernel | 100.00% | 32/32 |
| memory | 100.00% | 76/76 |
| reconstruction | 100.00% | 55/55 |
| replay | 100.00% | 131/131 |
| orchestration | 100.00% | 3/3 |
| semantic | 99.44% | 529/532 |
| workflows | 98.77% | 481/487 |
| kernel_runtime | 98.67% | 297/301 |
| determinism | 98.55% | 68/69 |
| crypto | 98.51% | 66/67 |
| persistence | 98.45% | 254/258 |
| execution | 98.25% | 562/572 |
| connectors_runtime | 98.21% | 165/168 |
| synchronization | 98.15% | 477/486 |
| evolution | 98.49% | 523/531 |
| connectors | 97.44% | 76/78 |
| query | 96.87% | 433/447 |
| runtime_memory_family | 95.51% | 617/646 |
| causality | 93.39% | 608/651 |
| reconstruction_runtime | 93.27% | 582/624 |

Every package is ≥93%.

## Uncovered lines (explained — not hidden)

| File | Coverage | Uncovered | Why |
|------|---------:|-----------|-----|
| `determinism/normalization.dart` | 85.7% (6/7) | the `return normalizeRuntimeValueCore(value)` fallback after the Node NFKC subprocess | Only reached when the `node` subprocess throws/exits non-zero. Node is on PATH in CI and dev, so the NFKC path always succeeds; Dart's `Platform.environment` is immutable at runtime, so the branch can't be forced without spawning a stripped-PATH child process. Pure-Dart CRLF/volatile normalization is fully covered. |

The remaining ~170 uncovered lines across the family packages are defensive fallbacks (`?? default` on values producers always supply, bounded-`sublist` truncation guards that trigger only at 5k–20k+ elements, value-type coercion arms the engines never emit) and the documented non-empty-HTML `UnsupportedError` paths in `semantic_engines.dart`. None are core API logic; every public API path is exercised.
