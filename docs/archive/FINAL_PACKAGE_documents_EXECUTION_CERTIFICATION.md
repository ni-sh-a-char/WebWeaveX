# FINAL PACKAGE DOCUMENTS EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 116 |
| PASS | 24 |
| FAIL | 91 |
| UNTESTED | 1 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/documents/api_documentation_engine.py` — py=None js=m is not defined
- `core/documents/architecture_document_engine.py` — py=None js=m is not defined
- `core/documents/argument_dependency_engine.py` — py=None js=ln is not defined
- `core/documents/argument_graph_engine.py` — py=None js=u is not defined
- `core/documents/argument_semantics_engine.py` — py=None js=ln is not defined
- `core/documents/argument_structure_engine.py` — py=None js=h is not defined
- `core/documents/citation_extraction_engine.py` — py=None js=CITATION_PATTERN.findall is not a function
- `core/documents/citation_grounding_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/documents/code_reference_engine.py` — py=None js=lang is not defined
- `core/documents/concept_graph_engine.py` — py=None js=The requested module '../index.js' does not provide an export named 'parseSource'
- `core/documents/concept_progression_engine.py` — py=None js=u is not defined
- `core/documents/concept_transition_engine.py` — py=None js=u is not defined
- `core/documents/conceptual_transition_engine.py` — py=None js=u is not defined
- `core/documents/coreference_graph_engine.py` — py=None js=p is not defined
- `core/documents/coreference_resolution_engine.py` — py=None js=p is not defined
- `core/documents/discourse_causality_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\documents\discourseDependencyEngine.ts:13:6: ERROR: Expected identifier but found "extends"
- `core/documents/discourse_dependency_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\documents\discourseDependencyEngine.ts:13:6: ERROR: Expected identifier but found "extends"
- `core/documents/discourse_parser_engine.py` — py=None js=h is not defined
- `core/documents/discourse_state_engine.py` — py=None js=Cannot read properties of undefined (reading 'id')
- `core/documents/discourse_structure_engine.py` — py=None js=The requested module '../index.js' does not provide an export named 'structureCognition'
- `core/documents/discourse_transition_engine.py` — py=None js=u is not defined
- `core/documents/document_dependency_graph_engine.py` — py=None js=s is not defined
- `core/documents/document_intelligence.py` — py=None js=h is not defined
- `core/documents/document_reconstruction_engine.py` — py=None js=Cannot find module 'C:\Projects\WebWeaveX\src\documents\reconstruction.js' imported from C:\Projects\WebWeaveX\src\documents\documentReconstructionEngine.ts
- `core/documents/document_semantic_ir_engine.py` — py=None js=The requested module '../index.js' does not provide an export named 'structureCognition'
- `core/documents/document_structure_engine.py` — py=None js=text.splitlines is not a function
- `core/documents/document_table_engine.py` — py=None js=text.splitlines is not a function or its return value is not iterable
- `core/documents/explanation_chain_engine.py` — py=None js=The requested module '../index.js' does not provide an export named 'structureCognition'
- `core/documents/explanation_dependency_engine.py` — py=None js=The requested module '../index.js' does not provide an export named 'structureCognition'
- `core/documents/explanation_graph_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\documents\discourseDependencyEngine.ts:13:6: ERROR: Expected identifier but found "extends"
- `core/documents/explanation_structure_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\documents\discourseDependencyEngine.ts:13:6: ERROR: Expected identifier but found "extends"
- `core/documents/heading_engine.py` — py=None js=h is not defined
- `core/documents/instructional_flow_engine.py` — py=None js=s is not defined
- `core/documents/instructional_reasoning_engine.py` — py=None js=s is not defined
- `core/documents/instructional_semantics_engine.py` — py=None js=s is not defined
- `core/documents/intelligence/__init__.py` — barrel_export_mismatch:['extract_semantic_outline']
- `core/documents/intelligence/code_block_engine.py` — py=None js=b is not defined
- `core/documents/intelligence/knowledge_block_engine.py` — py=None js=ln is not defined
- `core/documents/intelligence/semantic_outline_engine.py` — py=None js=h is not defined
- `core/documents/intelligence/toc_engine.py` — py=None js=h is not defined

_…and 51 more FAIL_

## UNTESTED

- `core/documents/discourse_memory_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
