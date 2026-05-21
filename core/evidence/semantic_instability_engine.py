from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_instability(
    unstable_regions: List[str],
    entropy: Dict[str, Any],
    evidence: List[str],
) -> Dict[str, Any]:
    regions = list(unstable_regions)
    if entropy.get("entropy", 0) >= 0.2:
        regions.append("semantic:entropy_instability")
    return {
        "unstable": bool(regions) or len(evidence) < 2,
        "regions": sorted(set(regions)),
        "truth_pressure": round(entropy.get("entropy", 0) + (0.3 if len(evidence) < 2 else 0), 3),
        "preserved": True,
    }
