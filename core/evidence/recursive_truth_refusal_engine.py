from __future__ import annotations

from typing import Any, Dict, List


def refuse_recursive_stabilization(suppressed: List[Dict[str, Any]]) -> Dict[str, Any]:
    refusals = [{"target": s.get("reason", "closure"), "message": "recursive_truthfully_incomplete"} for s in suppressed]
    return {
        "recursive_truth_refusals": refusals,
        "recursive_stabilization_failures": [s.get("reason") for s in suppressed],
        "recursive_boundary_failures": [s.get("truth_boundary_violation", {}).get("type") for s in suppressed],
        "recursive_termination_reasons": sorted(set(r["message"] for r in refusals)),
    }
