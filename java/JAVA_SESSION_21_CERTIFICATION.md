# JAVA_SESSION_21_CERTIFICATION

**Tier-B start — `heal_selector` (empty-HTML portable contract), byte-exact.** Branch `java`.
Canon `9625f4a`. Phase 0 verified `HEAD == origin/java` (`37cdd71`); rebuilt live (started 92/128).

## Key intelligence (machine-derived)
Re-audit of the Tier-2 "bs4" family proved the bs4 coupling is an **eager-`__init__` import
artifact, not a runtime dependency** — `compile_document_ir` runs byte-exact with bs4 blocked at
call time. The real blocker is the **size** of the pure semantic-IR NLP engines (6.5k–9.5k lines),
not BeautifulSoup. See [`JAVA_BS4_CAMPAIGN_REALITY.md`](JAVA_BS4_CAMPAIGN_REALITY.md) (corrects the
lazy-import premise of `JAVA_BS4_DECOUPLE_PLAN.md`).

## Implemented (1)
`io.webweavex.adaptive.SelectorHealing#healSelector` — `heal_selector(selector, dom_nodes, html="")`
for the portable empty-HTML contract. With `html=""`, `build_semantic_anchor` parses an empty
document → no anchors → the `semantic_anchor` strategy never contributes, so the output is a pure,
bs4-independent function of `selector` + `dom_nodes` (text-anchor / attribute-anchor /
structural-fallback). Non-empty-HTML anchor healing is Tier-C (Soup engine). Zero new substrate.

## Proofs

| Gate | Result |
| --- | --- |
| Runtime purity | bs4 import-guard proof: empty-HTML path never calls BeautifulSoup |
| Parity | `CrossLanguageParityS21Test` **19/19** byte-exact (text/attr/structural/over-cap/unicode/long-slice) |
| Coverage | **96.685 % → 96.6853 %** (non-regressing) |
| Governance | validator **PASS 93/128**; matrix 93; MAPPING +1; `PROVEN_FLOOR` 92→93; manifest unchanged |
| Full suite | `mvn clean verify` **902/0/0** BUILD SUCCESS |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 92 | **93** |
| Remaining | 36 | **35** |
| Total tests | 883 | **902** |
| Coverage | 96.685 % | **96.6853 %** |
| `PROVEN_FLOOR` | 92 | **93** |

Next: the large pure semantic-IR NLP engine ports (`query_documents`/`reason_semantically` — each
multi-session) per `JAVA_BS4_CAMPAIGN_REALITY.md`. Mission active — 93/128.
