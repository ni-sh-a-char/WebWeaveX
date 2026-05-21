from __future__ import annotations

from typing import Any, Dict, List


def model_noninference(
    evidence: List[str],
    inferred: Dict[str, Any],
    observed: Dict[str, Any],
    reconciled: Dict[str, Any],
    min_evidence: int = 2,
) -> Dict[str, Any]:
    refused = []
    noninferences = []
    if len(evidence) < min_evidence and inferred:
        refused.extend(sorted(f"infer:{k}" for k in inferred.keys()))
        noninferences.append("entity_link_without_evidence")
    if reconciled != observed and len(evidence) < min_evidence:
        noninferences.append("reconcile_without_evidence")
        refused.append("reconcile:unsupported")
    if inferred and not observed:
        noninferences.append("inferred_without_observation")
    return {
        "noninferences": sorted(set(noninferences)),
        "refused_inferences": sorted(set(refused)),
        "boundary_conditions": [f"min_evidence={min_evidence}"],
        "suppression_basis": {"evidence_count": len(evidence), "allowed": len(evidence) >= min_evidence},
    }
