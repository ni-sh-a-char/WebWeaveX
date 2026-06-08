# FINAL PACKAGE SEMANTIC EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 49 |
| PASS | 22 |
| FAIL | 27 |
| UNTESTED | 0 |
| Hash mismatches | 7 |
| State mismatches | 7 |

## Behavioral mismatches

- `core/semantic/ambiguity_preservation_engine.py` — output_or_state_mismatch
- `core/semantic/ambiguity_reasoning_engine.py` — output_or_state_mismatch
- `core/semantic/application_semantics_engine.py` — py=None js=step is not defined
- `core/semantic/causality_semantics_engine.py` — py=None js=handoff is not defined
- `core/semantic/contradiction_engine.py` — output_or_state_mismatch
- `core/semantic/contradiction_lineage_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/semantic/contradiction_preservation_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/semantic/contradiction_resolution_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/semantic/contradiction_restraint_engine.py` — output_or_state_mismatch
- `core/semantic/document_semantics_engine.py` — py=None js=kind is not defined
- `core/semantic/domain_classification_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\semantic\domainClassificationEngine.ts:10:34: ERROR: Expected "]" but found "<"
- `core/semantic/entity_extraction_engine.py` — py=None js=pattern.search is not a function
- `core/semantic/evidence_reconciliation_engine.py` — py=None js=c is not defined
- `core/semantic/incompleteness_preservation_engine.py` — output_or_state_mismatch
- `core/semantic/ontology_engine.py` — py=None js=e is not defined
- `core/semantic/semantic_alignment_engine.py` — output_or_state_mismatch
- `core/semantic/semantic_checkpoint_engine.py` — py=None js=Cannot find module 'kaalka'
Require stack:
- C:\Projects\WebWeaveX\src\crypto\kaalkaV5Client.ts
- `core/semantic/semantic_conflict_engine.py` — py=None js=v is not iterable
- `core/semantic/semantic_diff_engine.py` — py=None js=item is not defined
- `core/semantic/semantic_divergence_engine.py` — py=None js=null is not iterable
- `core/semantic/semantic_memory_engine.py` — py=None js=Cannot find module 'kaalka'
Require stack:
- C:\Projects\WebWeaveX\src\crypto\kaalkaV5Client.ts
- `core/semantic/semantic_orchestrator.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\semantic\domainClassificationEngine.ts:10:34: ERROR: Expected "]" but found "<"
- `core/semantic/semantic_resolution_engine.py` — py=None js=c is not defined
- `core/semantic/semantic_uncertainty_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/semantic/table_semantics_engine.py` — py=None js=BeautifulSoup is not defined
- `core/semantic/ui_semantics_engine.py` — py=None js=BeautifulSoup is not defined
- `core/semantic/uncertainty_propagation_engine.py` — output_or_state_mismatch

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
