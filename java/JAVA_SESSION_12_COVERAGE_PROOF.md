# JAVA_SESSION_12_COVERAGE_PROOF

**Phase 8 — coverage from a clean build (`mvn clean verify`).** Actual JaCoCo values.

| Metric | Value |
| --- | ---: |
| Previous certified coverage (Session 11) | **96.29 %** |
| **Current coverage (Session 12)** | **96.35 %** |
| **Delta** | **+0.06 pp** |
| Covered instructions | 26,396 |
| Total instructions | 27,395 |
| Floor (CI) | 94.0 % |
| Required (> 96.29 %) | **met (96.35 %)** |

## New-code coverage

| Class | Coverage |
| --- | ---: |
| `io.webweavex.evolution.EvolutionRuntime` | **96.8 %** |

Reachable branches covered by the 49 parity vectors, including 17 **engine-level** sections +
3 extra branch-reach vectors (distributed-evolutions extend/slice, null-semantic patterns,
"type"-fallback entities). Residual = defensive coercion arms. No synthetic tests.

## Gate

96.35 % **>** 96.29 % previous. **Coverage increased.** PASS.
