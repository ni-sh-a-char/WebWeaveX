# FINAL PACKAGE INTERNET EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 58 |
| PASS | 14 |
| FAIL | 42 |
| UNTESTED | 2 |
| Hash mismatches | 10 |
| State mismatches | 10 |

## Behavioral mismatches

- `core/internet/__init__.py` — barrel_export_mismatch:['rank_by_authority', 'score_authority', 'canonicalize_sources', 'extract_citation_chain', 'detect_contradictions']
- `core/internet/authority_engine.py` — output_or_state_mismatch
- `core/internet/citation_chain_engine.py` — py=None js=i is not defined
- `core/internet/citation_lineage_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/citation_network_engine.py` — py=None js=i is not defined
- `core/internet/citation_verification_engine.py` — output_or_state_mismatch
- `core/internet/confidence_calibration_engine.py` — output_or_state_mismatch
- `core/internet/contradiction_engine.py` — py=None js=a is not defined
- `core/internet/corroboration_graph_engine.py` — py=None js=k is not defined
- `core/internet/cross_source_contradiction_engine.py` — py=None js=c is not defined
- `core/internet/evidence_conflict_engine.py` — py=None js=c is not defined
- `core/internet/evidence_consensus_engine.py` — py=None js=k is not defined
- `core/internet/evidence_reliability_engine.py` — output_or_state_mismatch
- `core/internet/evidence_weight_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/extraction_ranking_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\internet\extractionRankingEngine.ts:9:9: ERROR: Expected ")" but found ":"
- `core/internet/generated_content_detection_engine.py` — output_or_state_mismatch
- `core/internet/information_diffusion_engine.py` — output_or_state_mismatch
- `core/internet/intelligence/__init__.py` — barrel_export_mismatch:['canonicalize_source_set', 'score_freshness', 'score_trust', 'merge_semantic_sources', 'rank_crawl_priority']
- `core/internet/intelligence/extraction_ranking_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\internet\intelligence\extractionRankingEngine.ts:9:7: ERROR: Expected ")" but found ":"
- `core/internet/intelligence/freshness_engine.py` — output_or_state_mismatch
- `core/internet/intelligence/trust_engine.py` — py=TypeError: unsupported operand type(s) for +: 'set' and 'list' js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/lineage_engine.py` — py=None js=u is not defined
- `core/internet/merge_engine.py` — output_or_state_mismatch
- `core/internet/mirror_detection_engine.py` — py=None js=p is not defined
- `core/internet/probabilistic_trust_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/semantic_consensus_engine.py` — py=None js=c is not defined
- `core/internet/semantic_consensus_graph_engine.py` — py=None js=k is not defined
- `core/internet/semantic_consistency_engine.py` — py=None js=c is not defined
- `core/internet/semantic_corroboration_engine.py` — py=None js=c is not defined
- `core/internet/semantic_dedup_engine.py` — py=None js=k is not defined
- `core/internet/semantic_provenance_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/semantic_reliability_engine.py` — output_or_state_mismatch
- `core/internet/source_clustering_engine.py` — py=None js=h is not defined
- `core/internet/source_consistency_engine.py` — py=None js=s is not defined
- `core/internet/source_corroboration_engine.py` — py=None js=k is not defined
- `core/internet/source_lineage_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/source_lineage_graph_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/source_ranking_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\internet\sourceRankingEngine.ts:9:9: ERROR: Expected ")" but found ":"
- `core/internet/trust_calibration_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:
- `core/internet/trust_engine.py` — py=None js=Transform failed with 1 error:
C:\Projects\WebWeaveX\src\evidence\lineageEngine.ts:14:6: ERROR: Cannot use "continue" here:

_…and 2 more FAIL_

## UNTESTED

- `core/internet/evidence_weighting_engine.py` — no_python_functions
- `core/internet/semantic_merge_engine.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
