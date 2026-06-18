# JAVA_SESSION_13_COVERAGE_PROOF

**Phase 8 — coverage from a clean build (`mvn clean verify`).** Actual JaCoCo values.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 12) | **96.35 %** |
| **Current coverage (Session 13)** | **96.38 %** |
| **Delta** | **+0.03 pp** |
| Covered instructions | 30,790 |
| Total instructions | 31,947 |
| Floor (CI) | 94.0 % |
| Required (> 96.35 %) | **met (96.38 %)** |

## New-code coverage

| Class | Coverage |
| --- | ---: |
| `io.webweavex.causality.CausalityRuntime` | **96.5 %** (4,394 / 4,552) |

Reachable branches covered by the 44 parity vectors, including 17 **engine-level** sections
exercising each sub-engine directly against the Python oracle (empty/unicode/unknown-runtime/
bridges/notification/process/recovery cases). Residual = defensive coercion arms. No synthetic
tests.

## Gate

96.38 % **>** 96.35 % previous. **Coverage increased.** PASS.
