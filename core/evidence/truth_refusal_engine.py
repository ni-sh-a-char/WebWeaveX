from __future__ import annotations

from typing import Any, Dict, List


def refuse_unsupported_stabilization(suppressed: List[Dict[str, Any]]) -> Dict[str, Any]:
    refusals = [{"target": s.get("reason", "stabilization"), "message": "truthfully_incomplete"} for s in suppressed]
    return {
        "truth_refusals": refusals,
        "stabilization_failures": [s.get("reason") for s in suppressed],
        "truth_boundary_failures": [s.get("truth_boundary_violation", {}).get("type") for s in suppressed],
        "termination_reasons": sorted(set(r["message"] for r in refusals)),
    }
