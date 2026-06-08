# ARCHITECTURE MAP

**Measured:** 2026-06-08T11:52:19.121186+00:00

WebWeaveX is two independent implementations of one specification:
- **Python** (`origin/python` `core/`, pip product `webweavex`)
- **JavaScript** (`src/`, npm product `webweavex`)

JS: 1846 modules across 106 subsystems. Python: 1724 core modules across 104 subsystems.

## Subsystem map (JS `src/<sub>` ⇄ Python `core/<sub>`)

| Subsystem | JS modules (engines) | Python modules (engines) |
|-----------|----------------------|--------------------------|
| `(core root)` | 0 (0) | 17 (11) |
| `(root)` | 18 (11) | 0 (0) |
| `actors` | 2 (1) | 2 (1) |
| `adaptive` | 23 (19) | 21 (19) |
| `agents` | 13 (9) | 13 (9) |
| `application` | 21 (19) | 21 (19) |
| `archive` | 2 (1) | 2 (1) |
| `ast` | 6 (5) | 6 (5) |
| `auth` | 6 (5) | 6 (5) |
| `autonomy` | 21 (16) | 21 (16) |
| `browser` | 16 (3) | 6 (3) |
| `bytecode` | 3 (1) | 3 (1) |
| `causal_intelligence` | 21 (19) | 21 (19) |
| `causality` | 21 (19) | 21 (19) |
| `cognition` | 1 (1) | 0 (0) |
| `compiler` | 7 (1) | 7 (1) |
| `connectors` | 41 (19) | 21 (19) |
| `consensus` | 2 (1) | 2 (1) |
| `contracts` | 5 (0) | 5 (0) |
| `crawling` | 34 (28) | 34 (28) |
| `crdt` | 2 (1) | 2 (1) |
| `crypto` | 14 (7) | 12 (7) |
| `database` | 7 (5) | 7 (5) |
| `determinism` | 6 (0) | 4 (0) |
| `distributed` | 41 (35) | 27 (24) |
| `distributed_extraction` | 21 (17) | 21 (17) |
| `distributed_memory` | 3 (1) | 3 (1) |
| `documents` | 118 (108) | 116 (107) |
| `dom` | 2 (1) | 2 (1) |
| `engineering` | 21 (19) | 21 (21) |
| `evidence` | 224 (216) | 223 (216) |
| `evolution` | 21 (15) | 21 (15) |
| `evolution_runtime` | 21 (19) | 21 (19) |
| `execution` | 23 (19) | 21 (19) |
| `execution_physics` | 21 (19) | 21 (19) |
| `execution_reality` | 21 (18) | 21 (18) |
| `extract` | 29 (1) | 29 (1) |
| `extraction` | 2 (1) | 2 (1) |
| `federation` | 2 (1) | 2 (1) |
| `fetch` | 9 (0) | 9 (0) |
| `files` | 4 (3) | 4 (3) |
| `filesystem` | 2 (1) | 2 (1) |
| `graph` | 43 (31) | 37 (31) |
| `graph_intelligence` | 1 (0) | 1 (0) |
| `hypergraph` | 2 (1) | 2 (1) |
| `identity` | 21 (19) | 20 (18) |
| `index` | 2 (1) | 2 (1) |
| `ingestion` | 2 (1) | 2 (1) |
| `integrations` | 9 (0) | 9 (0) |
| `intelligence` | 8 (7) | 8 (7) |
| `interaction` | 9 (7) | 9 (7) |
| `internet` | 58 (56) | 58 (56) |
| `ipc` | 2 (1) | 2 (1) |
| `ir` | 36 (0) | 35 (0) |
| `kernel` | 22 (0) | 22 (0) |
| `knowledge` | 61 (53) | 61 (53) |
| `layout` | 2 (1) | 2 (1) |
| `llm` | 20 (1) | 20 (1) |
| `logging` | 1 (0) | 1 (0) |
| `media` | 1 (0) | 1 (0) |
| `memory` | 47 (33) | 39 (33) |
| `multimodal` | 2 (1) | 2 (1) |
| `native` | 31 (24) | 31 (24) |
| `navigation` | 4 (3) | 4 (3) |
| `network` | 2 (1) | 2 (1) |
| `normalize` | 2 (0) | 2 (0) |
| `observability` | 4 (3) | 4 (3) |
| `ocr` | 2 (1) | 2 (1) |
| `optimizer` | 2 (1) | 2 (1) |
| `orchestration` | 6 (3) | 6 (3) |
| `parsers` | 28 (24) | 26 (24) |
| `performance` | 8 (7) | 8 (7) |
| `persistence` | 4 (3) | 4 (3) |
| `plugins` | 5 (0) | 5 (0) |
| `presentation` | 2 (1) | 2 (1) |
| `process` | 2 (1) | 2 (1) |
| `quality` | 7 (6) | 7 (6) |
| `query` | 17 (14) | 17 (14) |
| `query_language` | 6 (0) | 6 (0) |
| `reasoning` | 9 (6) | 9 (6) |
| `reconstruction` | 25 (10) | 20 (10) |
| `replay` | 8 (1) | 2 (1) |
| `repository` | 138 (122) | 133 (122) |
| `runtime` | 58 (44) | 56 (44) |
| `runtime_graph` | 6 (5) | 6 (5) |
| `runtime_language` | 5 (0) | 5 (0) |
| `schemas` | 3 (0) | 3 (0) |
| `security` | 23 (8) | 23 (8) |
| `semantic` | 63 (48) | 49 (47) |
| `serialize` | 6 (3) | 6 (3) |
| `session` | 4 (2) | 4 (2) |
| `spreadsheets` | 2 (1) | 2 (1) |
| `ssa` | 3 (2) | 3 (2) |
| `stream` | 2 (1) | 2 (1) |
| `streaming` | 16 (8) | 13 (8) |
| `synchronization` | 21 (19) | 21 (19) |
| `tables` | 2 (1) | 2 (1) |
| `transactions` | 3 (1) | 3 (1) |
| `treesitter` | 6 (1) | 6 (1) |
| `typed_ir` | 5 (0) | 5 (0) |
| `universal` | 24 (23) | 24 (23) |
| `utils` | 2 (0) | 2 (0) |
| `vision` | 5 (3) | 4 (3) |
| `vm` | 7 (1) | 2 (1) |
| `workflows` | 20 (18) | 20 (18) |
| `worldModel` | 6 (0) | 0 (0) |
| `world_model` | 16 (13) | 16 (13) |

## Core subsystems (vision-aligned)

- **Universal Extraction**: `extract/`, `browser/`, `crawling/`, `documents/`, `multimodal/`, `repository/`, `connectors/`, `streaming/`
- **Universal Knowledge / Semantic**: `semantic/`, `ontology/`, `reasoning/`, `knowledge`, `evidence/`, `citation`/`parsers/`
- **Universal Runtime Graph**: `graph/`, `runtime_graph/`, `contracts/`, `ir/`
- **Universal Memory**: `memory/`, `reconstruction/`, `replay/`
- **Deterministic Execution**: `determinism/`, `crypto/` (Kaalka), `kernel/`, `execution/`, `vm/`
- **Orchestration / Distributed**: `orchestration/`, `distributed/`, `workflows/`, `synchronization/`, `adaptive/`
- **Runtime / Cognition / World model**: `runtime/`, `cognition/`, `worldModel/`, `world_model/`, `identity/`, `vision/`

## Public API surface

- Python: 128 names (`webweavex/__init__.py __all__`) — see `docs/specs/python_api_inventory.json`
- JavaScript: 229 runtime exports (`src/index.ts` + `src/publicApi.ts`) — see `docs/specs/javascript_api_inventory.json`
- Parity: 128/128 Python public names mapped to JS — see `docs/specs/api_parity_matrix.json`

## Pipelines

- JS canonical pipeline: `src/kernel/runtimePipeline.ts` (`runCanonicalPipeline`: ingestion → runtime phases → unified graph → fingerprint)
- Python canonical pipeline: `core/kernel/runtime_pipeline.py` (`run_canonical_pipeline`)
- Equivalence harness: `validation/equivalence/` against `specification/vectors` (authority)
