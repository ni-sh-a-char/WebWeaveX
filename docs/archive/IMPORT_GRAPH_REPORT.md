# IMPORT GRAPH REPORT

**Modules scanned:** 452

## Entry-point import health

- OK: `webweavex`
- OK: `core.kernel.runtime_pipeline`
- OK: `core.browser.universal_web_extraction_engine`

## Rules enforced

- `core/contracts/` — boundary types only
- `core/ir/__init__.py` — lazy exports (no parser cycle)
- `core/kernel/runtime_pipeline.py` — canonical orchestration path

## High fan-in modules (top 10)

- `core.evidence`: 22 inbound references
- `core.crypto.kaalka_runtime_engine`: 20 inbound references
- `core.crypto.kaalka_hash_engine`: 18 inbound references
- `core.runtime_graph.runtime_graph_engine`: 14 inbound references
- `core.llm.base_adapter`: 13 inbound references
- `core.crypto.kaalka_session_engine`: 11 inbound references
- `core.parsers.parser_registry`: 10 inbound references
- `core.parsers`: 9 inbound references
- `core.evidence.lineage_engine`: 7 inbound references
- `core.ir._base`: 7 inbound references