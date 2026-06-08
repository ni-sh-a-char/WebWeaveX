# FINAL PACKAGE CONNECTORS EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 21 |
| PASS | 5 |
| FAIL | 16 |
| UNTESTED | 0 |
| Hash mismatches | 2 |
| State mismatches | 3 |

## Behavioral mismatches

- `core/connectors/__init__.py` — barrel_export_mismatch:['extract_runtime_streams', 'save_live_runtime', 'load_live_runtime']
- `core/connectors/api_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/cicd_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/container_connector_engine.py` — py=AttributeError: 'dict' object has no attribute 'lower' js=None
- `core/connectors/docker_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/filesystem_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/ide_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/kafka_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/kubernetes_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/live_runtime_memory_engine.py` — py=None js=Path is not defined
- `core/connectors/live_runtime_orchestrator.py` — output_or_state_mismatch
- `core/connectors/mysql_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/postgres_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/redis_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/connectors/runtime_stream_connector_engine.py` — output_or_state_mismatch
- `core/connectors/sqlite_connector_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
