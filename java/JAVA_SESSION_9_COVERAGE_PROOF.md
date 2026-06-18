# JAVA_SESSION_9_COVERAGE_PROOF

**Phase 3 — coverage re-verified from a clean build.** Actual JaCoCo values from
`target/site/jacoco/jacoco.csv` after `mvn clean verify`.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 8) | **95.68 %** |
| **Current coverage (Session 9, clean build)** | **95.88 %** |
| **Delta** | **+0.20 pp** |
| Covered instructions | 16,421 |
| Total instructions | 17,127 |
| Coverage floor (CI) | 94.0 % |

## New-code coverage (Session 9)

| Class | Coverage |
| --- | ---: |
| `io.webweavex.execution.ExecutionRuntime` | **96.50 %** (3,996 / 4,141) |

The ExecutionRuntime residual (~145 instr) is defensive/unreachable-via-input branches
(e.g. `pyInt` String/Boolean coercions, `recover` non-empty-failed loop unreachable through the
orchestrator, a few `applyRuntimeTransition` else-arms). Reachable branches are covered by the
89 parity vectors, including the 51 **engine-level** vectors added specifically to exercise the
internal engines (Python oracle — no synthetic tests).

## Gate

Current (95.88 %) **≥** previous certified (95.68 %). **Coverage did NOT decrease.** Gate PASS.
