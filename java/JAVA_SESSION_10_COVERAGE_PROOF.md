# JAVA_SESSION_10_COVERAGE_PROOF

**Phase 8 — coverage from a clean build (`mvn clean verify`).** Actual JaCoCo values.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 9) | **95.88 %** |
| **Current coverage (Session 10)** | **96.13 %** |
| **Delta** | **+0.25 pp** |
| Covered instructions | 19,916 |
| Total instructions | 20,717 |
| Floor (CI) | 94.0 % |
| Mandatory target (95.89 %) | **met (96.13 %)** |

## New-code coverage

| Class | Coverage |
| --- | ---: |
| `io.webweavex.synchronization.SyncRuntime` | **97.2 %** (3,488 / 3,590) |

The ~102 residual instructions are defensive/unreachable-via-input branches (e.g. `pyInt`
String/Boolean coercions, a few `pyEquals` type-mismatch arms). All reachable branches are
covered by the 49 parity vectors — including the 16 **engine-level** sections added so each
sub-engine is exercised directly against the Python oracle (no synthetic tests).

## Gate

96.13 % **>** 95.88 % previous **and >** 95.89 % mandatory target. **Coverage increased.** PASS.
