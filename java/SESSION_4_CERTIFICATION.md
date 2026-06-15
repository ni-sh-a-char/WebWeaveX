# SESSION 4 CERTIFICATION — connector-runtime extraction

**Artifact:** `io.webweavex:webweavex:2.1.0` · **Status: PASS**

Machine-readable companion: [`SESSION_4_CERTIFICATION.json`](SESSION_4_CERTIFICATION.json).
Analysis: [`JAVA_SESSION_4_ANALYSIS.md`](JAVA_SESSION_4_ANALYSIS.md).

## Scope

The pure-deterministic, dependency-safe subset of the **Extraction** layer
(preferred order #1): the connector-runtime family. Each API is a bounded transform
over a caller-supplied `snapshot` — no network, no OS, no Soup/multimodal subsystem.

| API (manifest) | Java class | Canonical Python |
| --- | --- | --- |
| `extract_database_runtime` | `connectors.DatabaseConnectors` | `core.connectors.database_connector_engine` |
| `extract_api_runtime` | `connectors.ApiConnectors` | `core.connectors.api_connector_engine` |
| `extract_runtime_streams` | `connectors.StreamConnectors` | `core.connectors.runtime_stream_connector_engine` |
| `extract_telemetry_runtime` | `connectors.TelemetryConnector` | `core.connectors.telemetry_connector_engine` |

Supporting sub-engines ported (used by the above, not standalone manifest APIs):
postgres / mysql / sqlite / redis / graphql / grpc / kafka / websocket.

## Evidence

| Item | Value |
| --- | --- |
| Java parity-proven APIs | **17 → 21** / 128 |
| Session-4 golden vectors | **23** (byte-exact vs canonical Python) |
| Full suite | **208 tests, 0 failures, 0 errors** |
| Instruction coverage | **94.91 %** (9,585 / 10,099; floor 94 %) |
| Validator | `validate_java_manifest.py` → **PASS** |
| Matrix | `JAVA_PARITY_MATRIX.md` regenerated, 21 proven |
| CI floor | `PROVEN_FLOOR` raised 17 → 21 |

## Method (parity, not assertion)

`tools/gen_java_parity_vectors_s4.py` imports the four canonical engines from a
materialized `origin/python` checkout and records, per vector, the
`stable_serialize` of the output and its `compute_kaalka_hash`.
`CrossLanguageParityS4Test` reconstructs each input, recomputes in Java, and asserts
byte-equality on both. The vectors span defaults, full snapshots, the degraded /
unknown-type fallbacks, `int()`/`str()` coercion, code-point `sorted(key=str)`, and
every dispatch branch (graphql/grpc, kafka/redis/websocket/sse/queue).

Because Python ≡ JavaScript ≡ Dart is already certified, proving **Java ≡ Python**
proves **Java ≡ JS ≡ Dart** for these four APIs.

## Reproduce

```bash
cd java && mvn -B -ntp clean verify           # 208 tests, JaCoCo
python ../tools/validate_java_manifest.py      # governance gate
# regenerate vectors from a materialized python branch:
PYTHONPATH=/path/to/pycore python ../tools/gen_java_parity_vectors_s4.py \
    src/test/resources/parity/golden_vectors_s4.json
```
