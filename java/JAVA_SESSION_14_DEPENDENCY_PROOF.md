# JAVA_SESSION_14_DEPENDENCY_PROOF

**Phase 1 — per-API relative-aware dependency proof (re-run this session).** Tracer:
`tools/trace_imports_s5_relative.py`. Canon `origin/python` @ `9625f4a`.

| API | def module | closure | forbidden | class |
| --- | --- | ---: | ---: | --- |
| `build_stream_timeline` | `streaming/stream_replay_engine` | 1 m / 60 L | 0 | **CLEAN** |
| `replay_stream_events` | `streaming/stream_replay_engine` | 1 m / 60 L | 0 | **CLEAN** |
| `save_live_runtime` | `connectors/live_runtime_memory_engine` | 4 m / 304 L | 0 | **CLEAN** |
| `load_live_runtime` | `connectors/live_runtime_memory_engine` | 4 m / 304 L | 0 | **CLEAN** |
| `run_live_runtime` | `connectors/live_runtime_orchestrator` | 26 m / 1158 L | 0 | **CLEAN (parity caveat ↓)** |
| `extract_runtime_streams` | `connectors/runtime_stream_connector_engine` | 4 m | 0 | already proven (S7) |
| `stream_extract` | `streaming/streaming_pipeline` | — | **>0** | **BLOCKED** |
| `capture_websocket_frames` | `streaming/websocket_runtime_engine` | 2 m | 0 (but page-coupled) | **DEFERRED** |

## Blocked / deferred detail

- **`stream_extract`** → `streaming_pipeline` imports `from core.extract.pipeline import extract`
  → the bs4/lxml HTML extraction pipeline. **BLOCKED** by the bs4 barrier (same root cause as the
  ~26 semantic APIs). Not implementable until upstream lazy-import.
- **`capture_websocket_frames`** → reads attributes off a live Playwright `page`
  (`page._test_websocket_frames`). 0 forbidden *imports*, but it is browser-`page`-coupled and is
  **Deferred** in the certified cross-language manifest. Deferred here for the same reason
  (consistent with JS/Dart).

## run_live_runtime parity caveat (NOT a dependency block)

`run_live_runtime` is dependency-clean, but its output is **self-referential**:
`payload["memory"]["snapshots"]` is `payload` itself. `stable_serialize` therefore recurses
infinitely **in Python itself** — the whole object is not byte-exact-serializable (manifest
classification: *Partial*). Every *computed value* is serializable, so it is certified by
**projection parity**: each non-cyclic output path (`database`, `api`, `streams`, `filesystem`,
`containers`, `kubernetes`, `cicd`, `telemetry`, `ide`, `graph`, `sync_state`, `live_ir`,
`replay`, `memory.*` except `snapshots`) is compared byte-exact to the Python oracle. The Java
port reproduces the identical self-reference, so behavior is identical.

## Substrate

**Zero new substrate.** Reuses the certified connector engines
(`DatabaseConnectors`/`ApiConnectors`/`StreamConnectors`/`ContainerConnector`/
`KubernetesConnector`/`TelemetryConnector`/`IdeConnector`) + determinism/crypto/json. Two new
*internal* sub-engines ported in-class: `extract_filesystem_runtime`, `extract_cicd_runtime`
(not manifest APIs).
