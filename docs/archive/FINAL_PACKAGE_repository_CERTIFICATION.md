# FINAL PACKAGE REPOSITORY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 133 |
| PASS | 35 |
| FAIL | 98 |
| UNTESTED | 0 |
| Hash mismatches | 5 |
| State mismatches | 5 |

## Behavioral mismatches

- `core/repository/__init__.py` — barrel_export_mismatch:['ingest_repository', 'extract_repository']
- `core/repository/api_contract_reasoning_engine.py` — py=None js=p is not defined
- `core/repository/api_surface_engine.py` — py=None js=ParserRegistry.detect_language is not a function
- `core/repository/api_surface_reasoning_engine.py` — output_or_state_mismatch
- `core/repository/architecture_reasoning_engine.py` — py=None js=Cannot find module 'C:\Projects\WebWeaveX\src\repository\reconstruction.js' imported from C:\Projects\WebWeaveX\src\repository\repositoryReconstructionEngine.ts
- `core/repository/ast/ast_cognition_engine.py` — py=None js=parse_python_ast is not defined
- `core/repository/ast/go_ast_engine.py` — py=None js=m is not defined
- `core/repository/ast/java_ast_engine.py` — py=None js=m is not defined
- `core/repository/ast/python_ast_engine.py` — python_import:No module named 'core.repository.astthon_ast_engine'
- `core/repository/ast/rust_ast_engine.py` — py=None js=m is not defined
- `core/repository/async_execution_reasoner.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/repository/async_runtime_engine.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/repository/async_topology_engine.py` — py=None js=null is not iterable
- `core/repository/dependency_graph_engine.py` — py=None js=ln is not defined
- `core/repository/dependency_resolution_engine.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/repository/deployment_causality_engine.py` — py=None js=s is not defined
- `core/repository/deployment_runtime_engine.py` — py=None js=null is not iterable
- `core/repository/deployment_semantics_engine.py` — py=None js=s is not defined
- `core/repository/deployment_topology_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/distributed_dependency_engine.py` — py=None js=s is not defined
- `core/repository/distributed_runtime_graph_engine.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/repository/docker_semantic_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\repository\dockerSemanticEngine.ts:12:8: ERROR: The symbol "line" has already been declared
- `core/repository/domain_reconstruction_engine.py` — py=None js=k is not defined
- `core/repository/event_causality_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/event_flow_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/event_topology_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/execution_dependency_engine.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/repository/execution_flow_engine.py` — py=None js=i is not defined
- `core/repository/import_graph_engine.py` — py=None js=i is not defined
- `core/repository/infra_execution_engine.py` — py=None js=null is not iterable
- `core/repository/infra_relationship_engine.py` — py=None js=s is not defined
- `core/repository/infra_topology_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/intelligence/__init__.py` — barrel_export_mismatch:['extract_repository_ast']
- `core/repository/intelligence/architecture_reconstruction_engine.py` — py=None js=d is not defined
- `core/repository/intelligence/build_system_engine.py` — py=None js=k is not defined
- `core/repository/intelligence/call_graph_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/repository/intelligence/framework_detection_engine.py` — py=None js=Cannot read properties of null (reading 'some')
- `core/repository/intelligence/repository_ast_engine.py` — output_or_state_mismatch
- `core/repository/intelligence/repository_lineage_engine.py` — py=None js=e is not defined
- `core/repository/intelligence/symbol_graph_engine.py` — py=None js=i is not defined

_…and 58 more FAIL_

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
