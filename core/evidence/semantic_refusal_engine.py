from __future__ import annotations

from typing import Any, Dict, List


def refuse_unsupported_conclusions(
    noninferable_regions: List[str],
    suppressed_speculation: List[Dict[str, Any]],
) -> Dict[str, Any]:
    refusals = []
    for region in noninferable_regions:
        refusals.append({"target": region, "message": "cannot_determine"})
    for spec in suppressed_speculation:
        refusals.append({"target": spec.get("reason", "speculation"), "message": "cannot_determine"})
    return {
        "refusals": refusals,
        "terminated_inferences": [r["target"] for r in refusals],
        "termination_reasons": sorted(set(r["message"] for r in refusals)),
        "unsupported_regions": noninferable_regions,
    }
