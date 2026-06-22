# JAVA_SESSION_26_CERTIFICATION

**`run_application_cognition` — portable `html=""` contract, byte-exact.** Branch `java`. Canon
`9625f4a`. Phase 0 verified `HEAD == origin/java` (`d847832`); rebuilt live (started 96/128).

## Frontier audit (decision: PORTABLE)
`run_application_cognition` fans to 13 engines; 5 (ui/form/dashboard/navigation/recovery) call
BeautifulSoup. Empirical `html=""` execution (with bs4 blocked at call time) proved the output is
**bs4-independent**: ui all-empty, forms `{forms:[], form_count:0}`, dashboard all-empty
(update_interval 30), navigation derived only from `url`/`route_history`. So the output is
deterministic, serializable, and byte-exact for the `html=""` contract — same methodology that
unlocked `query_documents`, `heal_selector`, `run_semantic_runtime`.

## Implemented
`io.webweavex.application.ApplicationCognitionRuntime#runApplicationCognition` + 12 sub-engines
(ui/form/dashboard/navigation/recovery as html="" constants; state/transitions/action-graph/
workflow-graph/intent/context/remember pure), **reusing** the certified
`ObjectiveExecution.executeRuntimeObjective`. Zero new substrate. No stubs.

## Proofs

| Gate | Result |
| --- | --- |
| Portability | bs4 import-guard proof: html="" output bs4-independent |
| Parity | `CrossLanguageParityS26Test` **25/25** byte-exact (orchestrator + 11 engine sections) |
| Coverage | **96.813 % → 96.835 %** (ApplicationCognitionRuntime ≈ 96 %) |
| Governance | validator **PASS 97/128**; matrix 97; MAPPING +1; `PROVEN_FLOOR` 96→97; manifest unchanged |
| Full suite | `mvn clean verify` **1100/0/0** BUILD SUCCESS |
| Exhaustion | [`JAVA_REMAINING_SURFACE_V4.md`](JAVA_REMAINING_SURFACE_V4.md) — portable-pending now **EMPTY** |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 96 | **97** |
| Remaining | 32 | **31** |
| Total tests | 1075 | **1100** |
| Coverage | 96.813 % | **96.835 %** |
| `PROVEN_FLOOR` | 96 | **97** |

The portable surface is exhausted. Next strategic lever: the Tier-C lxml/bs4-parity Soup engine
(unblocks ~6 extraction APIs + kernel-aggregator fallout). The remaining condition-B/Playwright/OCR/
platform sets are non-portable without a Python-canon change. Mission active — 97/128.
