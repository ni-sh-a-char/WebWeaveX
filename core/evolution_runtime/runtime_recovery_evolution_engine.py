from __future__ import annotations

from typing import Any, Dict, List


def evolve_recovery_order(
    repairs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordering = sorted(
        repairs,
        key=lambda item: str(item.get("action", "")),
    )

    return {
        "recovery_order": [item.get("action", "") for item in ordering],
        "evolved": True,
        "bounded": True,
    }
