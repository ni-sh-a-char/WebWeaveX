from __future__ import annotations

from typing import Any, Dict, List


def model_noninferable_regions(
    inferred: Dict[str, Any],
    evidence: List[str],
    noninferences: List[str],
    *,
    min_evidence: int = 2,
) -> Dict[str, Any]:
    regions: List[str] = list(noninferences)
    if len(evidence) < min_evidence and inferred:
        regions.append("semantic:insufficient_evidence")
    if inferred and not evidence:
        regions.append("semantic:ungrounded_inference")
    voids = sorted(set(regions))
    return {
        "noninferable_regions": voids,
        "inference_voids": voids,
        "semantic_boundaries": {"min_evidence": min_evidence, "blocked": len(voids) > 0},
        "unsupported_scope": {"regions": voids, "count": len(voids)},
        "epistemic_limits": {"cannot_determine": len(voids) > 0, "reason": "insufficient_evidence" if voids else None},
    }
