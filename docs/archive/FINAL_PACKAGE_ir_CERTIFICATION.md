# FINAL PACKAGE IR EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 35 |
| PASS | 20 |
| FAIL | 15 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/ir/__init__.py` — barrel_export_mismatch:['annotations', 'TYPE_CHECKING', 'Any']
- `core/ir/api_ir.py` — py=None js=str is not defined
- `core/ir/browser_ir.py` — py=None js=_META_RE.findall is not a function
- `core/ir/document_ir.py` — py=None js=The requested module '../index.js' does not provide an export named 'structureCognition'
- `core/ir/execution_ir.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/ir/internet_ir.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/ir/knowledge_ir.py` — py=None js=str is not defined
- `core/ir/ontology_ir.py` — py=None js=str is not defined
- `core/ir/repository_ir.py` — py=None js=The requested module '../parsers/parserRegistry.js' does not provide an export named 'parseSource'
- `core/ir/repository_runtime_ir.py` — py=None js=item is not defined
- `core/ir/runtime_ir.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\graph\semanticCycleAnalysisEngine.ts:22:7: ERROR: Expected ")" but found ":"
- `core/ir/semantic_graph_ir.py` — py=None js=str is not defined
- `core/ir/semantic_query_ir.py` — py=None js=str is not defined
- `core/ir/topology_ir.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\graph\semanticCycleAnalysisEngine.ts:22:7: ERROR: Expected ")" but found ":"
- `core/ir/unified_runtime_ir.py` — py=None js=phases.includes is not a function

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
