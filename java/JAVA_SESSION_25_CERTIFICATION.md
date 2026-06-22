# JAVA_SESSION_25_CERTIFICATION

**`run_semantic_runtime` + `run_semantic_for_extraction` — portable `html=""` contract, byte-exact.**
Branch `java`. Canon `9625f4a`. Phase 0 verified `HEAD == origin/java` (`dc32f04`); rebuilt live
(started 94/128).

## Portable-contract proof
`run_semantic_runtime` calls `extract_table_semantics`/`extract_ui_semantics` (BeautifulSoup), but
on **`html=""`** BeautifulSoup parses an empty document and contributes nothing observable (verified:
tables `[]`; UI html-derived fields all empty/False; only the `actions` passthrough survives). The
output is therefore **bs4-independent, deterministic, and serializable** for the `html=""` contract.

## Implemented (2 APIs + 16 engines + IR)
`io.webweavex.semantic.SemanticRuntime` — `run_semantic_runtime`, `run_semantic_for_extraction` +
the pure engines (entity-extraction/resolution, domain, ontology, semantic-graph, document/table/UI/
repository/application/causality/workflow/browser/runtime semantics, alignment, diff) + IR. Reuses
the certified `SemanticReplay` (replay) and `ExecutionRuntime.buildUnifiedRuntimeGraph` (merge).
Zero new substrate.

## Proofs

| Gate | Result |
| --- | --- |
| Parity | `CrossLanguageParityS25Test` **36/36** byte-exact (2 orchestrator APIs + 16 engine sections) |
| Coverage | **96.774 % → 96.813 %** (SemanticRuntime 97.4 %) |
| Governance | validator **PASS 96/128**; matrix 96; MAPPING +2; `PROVEN_FLOOR` 94→96; manifest unchanged |
| Full suite | `mvn clean verify` **1075/0/0** BUILD SUCCESS |
| Exhaustion | [`JAVA_REMAINING_SURFACE_V3.md`](JAVA_REMAINING_SURFACE_V3.md) — 32 remaining, classified |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 94 | **96** |
| Remaining | 34 | **32** |
| Total tests | 1039 | **1075** |
| Coverage | 96.774 % | **96.813 %** |
| `PROVEN_FLOOR` | 94 | **96** |

Next: `run_application_cognition` (empirical html="" frontier check — last portable candidate).
Mission active — 96/128.
