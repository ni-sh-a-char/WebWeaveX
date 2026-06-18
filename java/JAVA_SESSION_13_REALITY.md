# JAVA_SESSION_13_REALITY

**Phase 0 — repository reality rebuilt (no trust of prior outputs).** `git fetch origin`;
`HEAD == origin/java` confirmed at session start (`9d6db64`); matrix regenerated, validator run,
ranking recomputed live.

| Metric | Value | Source |
| --- | ---: | --- |
| Total manifest APIs | 128 | `PARITY_MANIFEST.json` |
| **Java parity-proven** | **61** | validator (`PASS 61/128`) |
| Remaining | 67 | 128 − 61 |
| Clean-portable | ~22 | mass trace (59 baseline − 37 implemented S7–S13) |
| Forbidden-blocked | 42 | mass trace (re-proved) |
| Special | 3 | RuntimeKernel/__version__/version |
| Tests | 646 | `mvn clean verify` |
| Coverage | 96.38% | JaCoCo |

## Clean clusters (recomputed)

| Cluster | clean APIs | new substrate |
| --- | ---: | --- |
| `core.streaming` | 4 | none |
| `core.reconstruction` | 4 | none |
| `core.memory` | 4 | none |
| `core.identity` | 3 | none |
| `core.connectors` (live_runtime) | 3 | none |
| `core.interaction` | 2 | none |
| `core.auth` | 1 | none |
| `core.repository` | 1 | path-canon harness |

(`core.causality` = **implemented this slice**.)

## Blocked clusters / hierarchy

semantic/evidence/memory(bs4)/modal/application/native (~26, bs4 import barrier);
HTML/web extraction (~10); OCR (2). Top lever unchanged = upstream bs4-decouple.
Remaining clean sweep ~22 APIs → ~83/128 with no upstream change.
