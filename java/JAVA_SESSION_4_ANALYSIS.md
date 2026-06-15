# JAVA_SESSION_4_ANALYSIS

**Analysis before implementation — Session 4 dependency slice selection.**

Per [`JAVA_BRANCH_POLICY.md`](../JAVA_BRANCH_POLICY.md): no code before analysis; every
API ported from Python canon with Python-generated golden vectors and a parity test.

## Mission preferred order vs. dependency reality

The mission's preferred implementation order is:

1. **Extraction** ← *this session targets the portable entry point here*
2. Repository extraction
3. Document extraction
4. Semantic extraction
5. Workflow layer
6. Vision
7. OCR

"Extraction" in WebWeaveX is **not** a single thing. Reading the canonical Python `core`
(materialized from `origin/python`), the extraction surface splits into three
dependency classes:

| Sub-family | Canonical modules | Portability |
| --- | --- | --- |
| **Live web / browser** (`extract_web`, `crawl`, `extract_infinite_scroll`, …) | `core/browser/*`, `core/fetch/*` | **Partial/Deferred** — network + live-browser side effects; out of certification scope |
| **HTML / document / repository** (`extract`, `extract_repository`, `compile_document`) | `core/extraction/*`, `core/dom/*`, `core/parsers/*` | **Heavy subsystem** — needs the full BeautifulSoup-parity Soup engine (a multi-session port); not completable in one slice without stubs |
| **Connector runtime** (`extract_database_runtime`, `extract_api_runtime`, `extract_runtime_streams`, `extract_telemetry_runtime`) | `core/connectors/*` | **Pure deterministic** — transforms a caller-supplied snapshot dict into a bounded runtime envelope; no network, no OS, no Soup, no multimodal |

### Why the connector-runtime family is the correct next slice

1. **Fully completable, no stubs.** Every function is a deterministic dict/list
   transform over a provided `snapshot`. Verified by reading every module
   (`telemetry_connector_engine.py` has **zero** `core.*` imports; the rest fan out only
   to sibling connector engines, all equally pure).
2. **Dependency-safe.** It depends only on the already-proven determinism + crypto
   foundation (the envelope is hashed via `stable_serialize` + `compute_kaalka_hash`,
   both byte-exact in Java since Session 1). No new subsystem is required.
3. **Classified `Complete` in `PARITY_MANIFEST.json`**, and four members of the broader
   extract family are in `executable_proven_apis` — these are first-class, certified APIs.
4. **It is genuinely "Extraction."** It is the portable subset of preferred-order #1,
   letting the branch advance into the Extraction layer this session while the
   Soup-dependent HTML path is correctly deferred to a dedicated multi-session effort
   (not faked with a placeholder).
5. **Rejected alternatives:** `ingest_input` (image branch pulls in the multimodal
   subsystem → would force a `Partial`); `run_canonical_pipeline`/`extract_web`
   (`Partial` by design — live side effects); HTML `extract` (needs the Soup engine).

## Scope of this slice

Package **`io.webweavex.connectors`** — 4 public APIs + 8 supporting sub-engines:

| Public API (manifest) | Java class | Python canon |
| --- | --- | --- |
| `extract_database_runtime` | `connectors.DatabaseConnectors` | `core.connectors.database_connector_engine` (+ postgres/mysql/sqlite/redis) |
| `extract_api_runtime` | `connectors.ApiConnectors` | `core.connectors.api_connector_engine` (+ graphql/grpc) |
| `extract_runtime_streams` | `connectors.StreamConnectors` | `core.connectors.runtime_stream_connector_engine` (+ kafka/websocket/redis) |
| `extract_telemetry_runtime` | `connectors.TelemetryConnector` | `core.connectors.telemetry_connector_engine` |

Supporting sub-engines ported (not standalone manifest APIs, used by the above):
`extract_postgres_runtime`, `extract_mysql_runtime`, `extract_sqlite_runtime`,
`extract_redis_runtime`, `extract_graphql_runtime`, `extract_grpc_runtime`,
`extract_kafka_runtime`, `extract_websocket_runtime`.

This raises Java parity-proven APIs **17 → 21**.

## Parity-critical Python semantics to reproduce exactly

The envelope is compared via `stable_serialize` + `compute_kaalka_hash`, which **sort
object keys** — so map key *order* is irrelevant, but **list element order and values
must match exactly**:

1. **`sorted(xs, key=str)`** (postgres/mysql/sqlite `tables`, graphql `types`, grpc
   `services`/`methods`, kafka `topics`, api `endpoints`) and plain **`sorted(...)`**
   (telemetry `backends`, `stream_types`) → stable sort by Unicode **code-point** order.
   Reproduced with `List.sort(Normalization::codePointCompare)` over `Py.str` (stable;
   identical to `key=str` for string lists).
2. **`int(...)`** coercion (`active_connections`, redis `clients`, websocket `frames`) →
   truncate-toward-zero to `long`.
3. **`str(...)`** coercion (`replication_state`, `propagation_state`) → `Py.str`.
4. **`list(...)` / `dict(...)` copies** with defaults (e.g. postgres `schemas` default
   `["public"]`, sqlite `schemas` always `["main"]`, graphql `endpoints` default
   `["/graphql"]`).
5. **List slicing** — redis `tables` `[:1000]`, telemetry `spans`/`logs` `[:10000]`.
6. **`snapshot.get(k, default)`** returns the raw value (passed through, incl.
   non-bool `degraded`).
7. **Dispatch + fallback** — `extract_database_runtime` wraps dispatch in try/except →
   `_degraded_database`; unknown type → degraded. `extract_runtime_streams` skips
   unknown stream types (no entry appended); `sse`/`queue` get a generic descriptor.

## Deliverables (per policy §3)

1. Java implementation in `io.webweavex.connectors` (no stubs/TODOs).
2. `tools/gen_java_parity_vectors_s4.py` — imports the four canonical engines, records
   `stable_serialize` + `compute_kaalka_hash` for a spread of snapshots (defaults, full,
   degraded, unknown-type, slicing boundaries).
3. `golden_vectors_s4.json` + `CrossLanguageParityS4Test` (byte-exact assertions).
4. Regenerated `JAVA_PARITY_MATRIX.md` (4 new `Implemented (parity-proven)` rows; total 21).
5. `validate_java_manifest.py` mapping extended (+4 entries); `connectors` package added
   to the matrix's documented package structure.
6. CI floors raised: `PROVEN_FLOOR` 17 → 21.
7. `SESSION_4_CERTIFICATION.{md,json}`.
