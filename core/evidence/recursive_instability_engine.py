from __future__ import annotations

from typing import Any, Dict, List


def model_recursive_instability(
    unstable_regions: List[str],
    depth: int,
    evidence_count: int,
) -> Dict[str, Any]:
    regions = list(unstable_regions)
    if depth > 2:
        regions.append(f"recursive:depth_{depth}_instability")
    if evidence_count < 2:
        regions.append("recursive:weak_evidence")
    return {
        "preserved": True,
        "unstable": bool(regions),
        "regions": sorted(set(regions)),
        "depth": depth,
    }
