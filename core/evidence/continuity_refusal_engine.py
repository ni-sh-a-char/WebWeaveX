from __future__ import annotations

from typing import Any, Dict, List


def refuse_unsupported_continuity(unsupported_continuity: List[Dict[str, Any]]) -> Dict[str, Any]:
    refusals = [{"target": r.get("reason", "continuity"), "message": "continuity_refused"} for r in unsupported_continuity]
    return {
        "continuity_refusals": refusals,
        "termination_reasons": sorted(set(r["message"] for r in refusals)),
        "boundary_failures": [r.get("reason") for r in unsupported_continuity],
    }
