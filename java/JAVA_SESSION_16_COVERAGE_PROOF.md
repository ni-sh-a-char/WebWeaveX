# JAVA_SESSION_16_COVERAGE_PROOF

`mvn clean verify` JaCoCo.

| Metric | Value |
| --- | ---: |
| Previous (S15) | **96.405 %** |
| **Current (S16)** | **96.419 %** |
| Covered / total | 36,346 / 37,696 |
| Required (> 96.405 %) | **met** |

`ReconstructionRuntime` reached ≈ 96.5 % via 43 parity vectors (2 orchestrator APIs, 16
engine-level sections incl. comparator-tier/null-runtime-fabricate/string+bool-tick vectors,
snapshot save/load). Residual = unreachable defensive code (IOException catches, `capped`
overflow). **Coverage increased — PASS.**
