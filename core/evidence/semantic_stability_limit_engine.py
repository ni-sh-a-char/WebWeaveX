from __future__ import annotations

from typing import Any, Dict


def semantic_stability_limits(stability: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "max_confidence": stability.get("stability_limits", {}).get("max_confidence", 0.5),
        "expansion_allowed": stability.get("stable", False),
    }
