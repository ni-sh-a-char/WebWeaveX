# JAVA_SESSION_11_COVERAGE_PROOF

**Phase 8 — coverage from a clean build (`mvn clean verify`).** Actual JaCoCo values.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 10) | **96.13 %** |
| **Current coverage (Session 11)** | **96.29 %** |
| **Delta** | **+0.16 pp** |
| Covered instructions | 22,909 |
| Total instructions | 23,791 |
| Floor (CI) | 94.0 % |
| Required (> 96.13 %) | **met (96.29 %)** |

## New-code coverage

| Class | Coverage |
| --- | ---: |
| `io.webweavex.workflow.WorkflowRuntime` | **97.1 %** (2,986 / 3,074) |

The ~88 residual instructions are defensive/unreachable-via-input branches (`pyInt`
String/Boolean coercions, a few default arms). All reachable branches are covered by the 50
parity vectors, including the 13 **engine-level** sections exercising each sub-engine directly
against the Python oracle (no synthetic tests).

## Gate

96.29 % **>** 96.13 % previous. **Coverage increased.** PASS.
