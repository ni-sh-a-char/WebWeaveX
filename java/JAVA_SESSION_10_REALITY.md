# JAVA_SESSION_10_REALITY

**Phase 0 — repository reality rebuilt (no trust of prior outputs).** `git fetch origin`;
`HEAD == origin/java` confirmed at session start (`6163cee`); matrix regenerated, validator run,
dependency tracing + ranking recomputed live.

## Counts (post-slice)

| Metric | Value | Source |
| --- | ---: | --- |
| Total manifest APIs | 128 | `PARITY_MANIFEST.json` |
| **Java parity-proven** | **43** | validator (`PASS 43/128`) |
| Remaining | 85 | 128 − 43 |
| Clean-portable | ~40 | mass trace (59 baseline − 19 implemented S7–S10) |
| Forbidden-blocked | 42 | mass trace (re-proved) |
| Special | 3 | RuntimeKernel/__version__/version |
| Tests | 503 | `mvn clean verify` |
| Coverage | 96.13% | JaCoCo |

## Clean clusters (recomputed ranking)

| Cluster | clean APIs | new substrate |
| --- | ---: | --- |
| `core.workflows` | 7 | none |
| `core.evolution_runtime` | 6 | none |
| `core.causality` | 5 | none |
| `core.streaming` | 4 | none |
| `core.reconstruction` | 4 | none |
| `core.memory` | 4 | none |
| `core.identity` | 3 | none |
| `core.connectors` (live_runtime) | 3 | none |
| `core.interaction` | 2 | none |
| `core.auth` | 1 | none |
| `core.repository` | 1 | path-canon harness |

(`core.synchronization` = **implemented this slice**; `core.execution` = S9.)

## Blocked clusters

semantic/evidence/memory(bs4)/modal/application/native (~26, bs4 import barrier);
HTML/web extraction (~10, lxml/network/browser); OCR (2). Leverage ranking unchanged — top
lever remains the upstream bs4-decouple.

## Leverage ranking (next clean target)

`core.workflows` (7, zero substrate) is the highest parity-surface reduction; selected for
Session 11 (see `JAVA_SESSION_11_PLAN.md`).
