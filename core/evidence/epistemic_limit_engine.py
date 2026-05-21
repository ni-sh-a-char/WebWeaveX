from __future__ import annotations

from typing import Any, Dict, List


def model_epistemic_limits(
    evidence: List[str],
    parser_density: int,
    fragility: Dict[str, Any],
) -> Dict[str, Any]:
    cannot_conclude = []
    if len(evidence) < 2:
        cannot_conclude.append("definitive_semantic_conclusion")
    if parser_density == 0:
        cannot_conclude.append("parser_grounded_conclusion")
    if fragility.get("level") == "high":
        cannot_conclude.append("high_confidence_claim")
    return {
        "cannot_conclude": sorted(set(cannot_conclude)),
        "exceeds_evidence": len(evidence) < 1,
        "exceeds_parser_grounding": parser_density == 0,
        "exceeds_corroboration": len(evidence) < 2,
        "max_confidence": fragility.get("confidence_limits", {}).get("max_score", 0.5),
    }
