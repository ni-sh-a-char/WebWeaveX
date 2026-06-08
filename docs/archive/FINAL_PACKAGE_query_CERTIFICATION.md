# FINAL PACKAGE QUERY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 17 |
| PASS | 4 |
| FAIL | 13 |
| UNTESTED | 0 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/query/__init__.py` — barrel_export_mismatch:['query_semantics', 'query_repository', 'query_documents', 'query_graph', 'query_knowledge']
- `core/query/discourse_query_engine.py` — py=None js=next is not defined
- `core/query/document_query_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/query/graph_query_engine.py` — py=None js=str is not defined
- `core/query/graph_scale_traversal_engine.py` — py=None js=deque is not defined
- `core/query/ontology_query_engine.py` — py=None js=str is not defined
- `core/query/repository_query_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts
- `core/query/runtime_query_engine.py` — output_or_state_mismatch
- `core/query/semantic_query_engine.py` — py=None js=str is not defined
- `core/query/semantic_resolution_engine.py` — py=None js=e is not defined
- `core/query/semantic_search_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\query\semanticSearchEngine.ts:13:10: ERROR: Expected ")" but found ":"
- `core/query/semantic_traversal_engine.py` — py=AttributeError: 'list' object has no attribute 'get' js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\query\semanticTraversalEngine.ts:42:7: ERROR: Expected ")" but found ":"
- `core/query/topology_query_engine.py` — py=AttributeError: 'list' object has no attribute 'get' js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\query\semanticTraversalEngine.ts:42:7: ERROR: Expected ")" but found ":"

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
