# FINAL PACKAGE PARSERS EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 26 |
| PASS | 3 |
| FAIL | 16 |
| UNTESTED | 7 |
| Hash mismatches | 0 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/parsers/__init__.py` — barrel_export_mismatch:['ParserRegistry', 'parse_source', 'ParserBudget', 'enforce_budget', 'recover_syntax']
- `core/parsers/api_resolution_engine.py` — py=None js=interfaces.update is not a function
- `core/parsers/call_graph_engine.py` — py=None js=c is not defined
- `core/parsers/dependency_resolution_engine.py` — py=None js=deps.update is not a function
- `core/parsers/formal_parser_grounding_engine.py` — py=None js=Cannot convert undefined or null to object
- `core/parsers/framework_resolution_engine.py` — py=None js=d is not defined
- `core/parsers/parser_budget_engine.py` — py=AttributeError: 'str' object has no attribute 'max_bytes' js=raw.slice(...).decode is not a function
- `core/parsers/parser_capability_engine.py` — py=None js=SUPPORTED.includes is not a function
- `core/parsers/parser_cognition_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/parsers/parser_output_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/parsers/parser_registry.py` — py=AttributeError: 'str' object has no attribute 'max_bytes' js=None
- `core/parsers/parser_streaming_engine.py` — py=None js=raw.slice(...).decode is not a function
- `core/parsers/repository_semantic_engine.py` — py=None js=ParserRegistry.parse is not a function
- `core/parsers/runtime_resolution_engine.py` — py=None js=d is not defined
- `core/parsers/semantic_graph_engine.py` — py=None js=nid is not defined
- `core/parsers/symbol_resolution_engine.py` — py=None js=interfaces.update is not a function

## UNTESTED

- `core/parsers/parser_recovery_engine.py` — no_python_functions
- `core/parsers/semantic_ast_engine.py` — no_python_functions
- `core/parsers/semantic_callgraph_engine.py` — no_python_functions
- `core/parsers/semantic_dependency_engine.py` — no_python_functions
- `core/parsers/semantic_import_engine.py` — no_python_functions
- `core/parsers/semantic_runtime_engine.py` — no_python_functions
- `core/parsers/semantic_symbol_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
