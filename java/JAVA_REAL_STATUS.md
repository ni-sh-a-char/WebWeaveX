# JAVA_REAL_STATUS

**Machine-derived parity status of the `java` branch. Everything below is computed from
repository state** (`PARITY_MANIFEST.json`, `tools/validate_java_manifest.py` MAPPING,
`tools/rank_remaining_apis.result.json` from the relative-aware dependency tracer), not
estimated.

## Counts (as of this slice)

| Metric | Value | Source |
| --- | ---: | --- |
| Total manifest APIs | 128 | `PARITY_MANIFEST.json` |
| **Java parity-proven** | **27** | validator MAPPING (`PASS 27/128`) |
| Remaining | 101 | 128 − 27 |
| — clean-portable (0 forbidden deps) | **56** | mass trace (59 clean − 3 implemented this slice) |
| — forbidden-blocked | **42** | mass trace |
| — special (RuntimeKernel, `__version__`, `version`) | 3 | manifest (class/const, not snapshot fns) |
| Manifest Complete / Partial / Deferred (P/JS/Dart) | 105 / 18 / 5 | `PARITY_MANIFEST.json` counts |

## Completion percentages (machine-derived)

| Measure | % |
| --- | ---: |
| Branch completion (proven / total) | **21.1 %** (27/128) |
| Parity completion of the *portable* surface (proven / (proven + clean-remaining)) | **32.5 %** (27/83) |
| Forbidden-blocked share of remaining | 41.6 % (42/101) |

The 42 forbidden-blocked APIs are **not** Java-fault — they transitively import a forbidden
runtime in the **canonical Python** (overwhelmingly BeautifulSoup via the eager
`core.evidence`/`core.semantic` package `__init__`; see
[`JAVA_NEXT_TARGET_RANKING.md`](JAVA_NEXT_TARGET_RANKING.md) and
[`JAVA_SESSION_6_BLOCKER_AUDIT.md`](JAVA_SESSION_6_BLOCKER_AUDIT.md)). They are blocked until
the canon decouples those imports or the gate adopts a behavioral criterion.

## Subsystem completion (proven APIs per subsystem)

| Subsystem (Java package) | Proven | Notes |
| --- | ---: | --- |
| determinism + crypto | foundation | byte-exact (Normalization/StableSerialize/Kaalka) |
| kernel / graph / ir / persistence / replay | 5 | S2 |
| query / memory / reconstruction | 8 | S3 |
| connectors | **7** | S4 (db/api/streams/telemetry) + S7 (container/ide/kubernetes) |
| documents / interaction | 3 | S4B (`extract_document_runtime`, `extract_paginated_content`) + S6 (`build_interaction_graph`) |

## Proven API list (27)

`UniversalInput, build_interaction_graph, build_runtime_graph, build_runtime_memory,
compile_unified_runtime_ir, compute_global_runtime_fingerprint, compute_kaalka_hash,
decrypt_value, encrypt_value, extract_api_runtime, extract_container_runtime,
extract_database_runtime, extract_document_runtime, extract_ide_runtime,
extract_kubernetes_runtime, extract_paginated_content, extract_runtime_streams,
extract_telemetry_runtime, fingerprint, query_graph, query_knowledge, query_runtime_graph,
query_runtime_memory, reconstruct_runtime, search_runtime_memory,
validate_reconstructed_runtime, validate_replay_equivalence`

## Reproduce

```
python tools/validate_java_manifest.py            # -> PASS 27/128
python tools/gen_java_parity_matrix.py            # regenerates JAVA_PARITY_MATRIX.md (27)
# remaining-API ranking (needs a materialized python checkout):
python tools/rank_remaining_apis.py               # -> tools/rank_remaining_apis.result.json
```
