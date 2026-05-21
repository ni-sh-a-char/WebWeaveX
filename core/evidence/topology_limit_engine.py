from __future__ import annotations

from typing import Any, Dict


def topology_limits(boundaries: Dict[str, Any]) -> Dict[str, Any]:
    return {"propagation": boundaries.get("propagation_allowed", False), "deployment": boundaries.get("deployment_inference_allowed", False)}
