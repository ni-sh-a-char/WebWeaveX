# JAVA_SESSION_14_COVERAGE_PROOF

**Phase 8 — coverage from a clean build (`mvn clean verify`).** Actual JaCoCo values.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 13) | **96.38 %** |
| **Current coverage (Session 14)** | **96.40 %** |
| Covered instructions | 32,639 |
| Total instructions | 33,859 |
| Floor (CI) | 94.0 % |
| Required (> 96.38 %) | **met (96.397 %)** |

## New-code coverage

| Class | Coverage |
| --- | ---: |
| `io.webweavex.streaming.StreamingRuntime` | **96.3 %** |

Coverage is via the 34 parity vectors, including projection vectors for the orchestrator,
a root-normalized FS-walk vector for the null-snapshot branch, and string/boolean-timestamp +
null-input + defensive-arm vectors. Residual ≈ unreachable defensive code (IOException catches,
`capped` overflow >10 000, the filesystem degraded-`catch`) — none reachable by any input.

## Gate

96.40 % **>** 96.38 % previous. **Coverage increased.** PASS.
