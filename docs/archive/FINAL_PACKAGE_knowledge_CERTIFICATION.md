# FINAL PACKAGE KNOWLEDGE EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 61 |
| PASS | 18 |
| FAIL | 43 |
| UNTESTED | 0 |
| Hash mismatches | 5 |
| State mismatches | 5 |

## Behavioral mismatches

- `core/knowledge/__init__.py` — barrel_export_mismatch:['build_repository_knowledge', 'build_service_relationships', 'build_dependency_lineage', 'build_framework_relationships', 'build_execution_flow']
- `core/knowledge/civilization_ontology_engine.py` — py=None js=e is not defined
- `core/knowledge/dependency_lineage_engine.py` — py=None js=i is not defined
- `core/knowledge/entity_resolution_engine.py` — py=None js=e is not defined
- `core/knowledge/execution_flow_engine.py` — py=None js=f is not defined
- `core/knowledge/graph_reasoning_engine.py` — py=None js=n is not defined
- `core/knowledge/knowledge_reconciliation_runtime.py` — py=None js=t is not defined
- `core/knowledge/knowledge_reconstruction_engine.py` — py=None js=Cannot find module 'C:\Projects\WebWeaveX\src\knowledge\reconstruction.js' imported from C:\Projects\WebWeaveX\src\knowledge\knowledgeReconstructionEngine.ts
- `core/knowledge/ontology_conflict_engine.py` — py=None js=t is not defined
- `core/knowledge/ontology_conflict_runtime.py` — py=None js=t is not defined
- `core/knowledge/ontology_consistency_engine.py` — output_or_state_mismatch
- `core/knowledge/ontology_contradiction_engine.py` — py=None js=t is not defined
- `core/knowledge/ontology_diff_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\knowledge\ontologyDiffEngine.ts:10:7: ERROR: Expected ")" but found ":"
- `core/knowledge/ontology_engine.py` — py=None js=The requested module '../evidence/unsupportedStabilizationEngine.js' does not provide an export named '_stabilizationRecord'
- `core/knowledge/ontology_entropy_engine.py` — output_or_state_mismatch
- `core/knowledge/ontology_evidence_engine.py` — py=None js=edge.includes is not a function
- `core/knowledge/ontology_evolution_engine.py` — py=None js=(pk & ck) is not iterable
- `core/knowledge/ontology_reconciliation_engine.py` — output_or_state_mismatch
- `core/knowledge/ontology_restraint_engine.py` — py=None js=The requested module '../evidence/unsupportedStabilizationEngine.js' does not provide an export named '_stabilizationRecord'
- `core/knowledge/ontology_self_confirmation_engine.py` — py=None js=The requested module '../evidence/unsupportedStabilizationEngine.js' does not provide an export named '_stabilizationRecord'
- `core/knowledge/ontology_validation_engine.py` — py=None js=e.includes is not a function
- `core/knowledge/reconstruction/__init__.py` — barrel_export_mismatch:['resolve_entities', 'build_semantic_identity', 'build_concept_graph', 'build_repository_knowledge', 'build_documentation_knowledge']
- `core/knowledge/reconstruction/architecture_knowledge_engine.py` — py=None js=e is not defined
- `core/knowledge/reconstruction/concept_graph_engine.py` — py=None js=i is not defined
- `core/knowledge/reconstruction/dependency_knowledge_engine.py` — py=None js=i is not defined
- `core/knowledge/reconstruction/documentation_knowledge_engine.py` — py=None js=s is not defined
- `core/knowledge/reconstruction/repository_knowledge_engine.py` — py=None js=i is not defined
- `core/knowledge/reconstruction/semantic_identity_engine.py` — py=None js=n.encode is not a function
- `core/knowledge/recursive_ontology_lock_engine.py` — py=None js=The requested module '../evidence/recursiveSemanticClosureEngine.js' does not provide an export named '_closureRecord'
- `core/knowledge/repository_knowledge_engine.py` — py=None js=i is not defined
- `core/knowledge/semantic_causality_engine.py` — py=None js=The requested module '../evidence/unsupportedStabilizationEngine.js' does not provide an export named '_stabilizationRecord'
- `core/knowledge/semantic_corroboration_engine.py` — py=None js=Cannot convert undefined or null to object
- `core/knowledge/semantic_dependency_engine.py` — py=None js=The requested module '../evidence/unsupportedStabilizationEngine.js' does not provide an export named '_stabilizationRecord'
- `core/knowledge/semantic_graph_engine.py` — py=None js=e is not defined
- `core/knowledge/semantic_identity_calculus.py` — py=None js=namespacename.encode is not a function
- `core/knowledge/semantic_identity_continuity_engine.py` — py=None js=e is not defined
- `core/knowledge/semantic_identity_resolver.py` — py=None js=e is not defined
- `core/knowledge/semantic_identity_runtime.py` — py=None js=e is not defined
- `core/knowledge/semantic_merge_rigor_engine.py` — output_or_state_mismatch
- `core/knowledge/semantic_merge_validator.py` — py=None js=t is not defined

_…and 3 more FAIL_

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
