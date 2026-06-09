# TEST_VALIDATION_REPORT.md

> Measured on 2026-06-10 at HEAD `041f033`. Re-ran the full suite from a clean tree.

## Toolchain

| Tool | Version |
|------|---------|
| Dart SDK | 3.8.2 (stable) windows_x64 |
| `dart pub get` | Got dependencies (8 packages have newer majors held by constraints — non-blocking) |

## Static gates (pre-test)

| Gate | Command | Result |
|------|---------|--------|
| Format | `dart format --set-exit-if-changed .` | ✅ 0 changed (189 files) |
| Analyze | `dart analyze` | ✅ No issues found! (strict-casts + strict-inference) |

## Test execution

| Metric | Value |
|--------|-------|
| Command | `dart test` |
| Result | ✅ **All tests passed** |
| Passing | **802** (779 baseline + 14 `heal_selector` + 9 `replay_interactions` parity/branch tests) |
| Failing | **0** |
| Test files | 35 (`test/**/*.dart`) |
| Wall time | ~54 s |

The runner’s final line: `+802: All tests passed!`

## Coverage by category (test directories)

Tests span: crypto, determinism, graph, replay, memory, reconstruction, kernel,
browser, connectors, plus the 12 ported runtime-cognition families
(causality, semantic, synchronization, evolution, workflows, execution,
memory-runtime, reconstruction-runtime, persistence, connectors-runtime,
query, kernel/contracts/unified-IR) under `test/parity/` and `test/engines/`.

## Failures

**None.** Zero failing, zero skipped-due-to-error, zero flaky on this run.

## Verdict

Test gate **PASS**: 802/802 green, 0 failures, on a clean tree.
