from __future__ import annotations

from typing import Any, Dict, List, Optional


def model_inference_integrity(
    evidence: List[str],
    supporting: List[str],
    contradicting: List[str],
    fragility: Dict[str, Any],
    missing_evidence: Optional[List[str]] = None,
) -> Dict[str, Any]:
    caps = fragility.get("confidence_limits", {})
    return {
        "basis": fragility.get("basis", {}),
        "supporting_evidence": sorted(set(supporting or evidence)),
        "contradicting_evidence": sorted(set(contradicting or [])),
        "missing_evidence": sorted(set(missing_evidence or fragility.get("missing_support", []))),
        "uncertainty_factors": fragility.get("contradiction_pressure", []),
        "confidence_caps": [caps.get("max_score", 1.0)],
        "unsupported_dimensions": fragility.get("missing_support", []),
        "fragility": fragility,
    }
