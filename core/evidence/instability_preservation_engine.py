from __future__ import annotations

from typing import Any, Dict, List


def preserve_instability(
    unstable_regions: List[str],
    evidence: List[str],
    stabilization_suppressed: List[Dict[str, Any]],
) -> Dict[str, Any]:
    regions = list(unstable_regions)
    if len(evidence) < 2:
        regions.append("semantic:weak_evidence_instability")
    if stabilization_suppressed:
        regions.append("semantic:stabilization_blocked")
    return {
        "preserved": True,
        "unstable": bool(regions),
        "regions": sorted(set(regions)),
        "do_not_stabilize": True,
    }
