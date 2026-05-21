from __future__ import annotations

from typing import Any, Dict


def topology_truth_limits(boundaries: Dict[str, Any]) -> Dict[str, Any]:
    return {"self_confirmation_allowed": False, "propagation": boundaries.get("propagation_allowed", False)}
