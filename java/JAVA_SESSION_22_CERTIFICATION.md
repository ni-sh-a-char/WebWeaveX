# JAVA_SESSION_22_CERTIFICATION

**Tier-B1 — `query_documents` + the 21 pure document semantic-IR engines, byte-exact.** Branch
`java`. Canon `9625f4a`. Phase 0 verified `HEAD == origin/java` (`9724af9`); rebuilt live (started
93/128).

## Breakthrough
The Tier-2 "bs4/epistemic wall" for `query_documents` was dissolved by finding the certification
frontier: the document path passes through `core.evidence.structure_cognition` (216-module /
4496-line epistemic engine) but **discards every epistemic-computed field** — proven empirically
(`query_documents` output contains none). So a **passthrough `structure_cognition`** + the 21 pure
document engines (~417 L) certify it byte-exact, with **no epistemic engine and no Python change**.
See [`JAVA_DOCUMENT_IR_CAMPAIGN.md`](JAVA_DOCUMENT_IR_CAMPAIGN.md).

## Implemented
`io.webweavex.documents.DocumentSemanticIr` — `query_documents` + `compile_document_ir` +
`build_document_semantic_ir` + 18 sub-engines (rhetorical/role/argument/discourse/transition/
progression/heading/section/instructional/tutorial/coreference/dependency-graph) + passthrough
`structure_cognition`. Faithful `splitlines`/`re`/`sorted(set)` semantics. Zero new substrate.

## Proofs

| Gate | Result |
| --- | --- |
| Runtime frontier | epistemic fields empirically absent from output → passthrough suffices |
| Parity | `CrossLanguageParityS22Test` **137/137** byte-exact (query_documents + 19 engine sections × 7 docs + reconstruct cases) |
| Coverage | **96.685 % → 96.774 %** (DocumentSemanticIr ≈ 96 %) |
| Governance | validator **PASS 94/128**; matrix 94; MAPPING +1; `PROVEN_FLOOR` 93→94; manifest unchanged |
| Full suite | `mvn clean verify` **1039/0/0** BUILD SUCCESS |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 93 | **94** |
| Remaining | 35 | **34** |
| Total tests | 902 | **1039** |
| Coverage | 96.685 % | **96.774 %** |
| `PROVEN_FLOOR` | 93 | **94** |

Next (high ROI): **`query_semantics`** — now only needs the `core.query.repository` engine +
`compile_semantic_query_ir` (its `document`/`graph`/`knowledge` paths are all proven). Mission
active — 94/128.
