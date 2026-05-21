from __future__ import annotations

from typing import Any, Dict, List


def forecast_semantic_change(
    changes: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        changes,
        key=lambda x: str(
            x.get("id")
        ),
    )

    return {
        "forecast": ordered,
        "forecast_size": len(
            ordered
        ),
    }
