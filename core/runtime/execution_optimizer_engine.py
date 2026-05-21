from __future__ import annotations

from typing import Any, Dict, List


def optimize_execution_order(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        tasks,
        key=lambda x: (
            x.get("weight", 0),
            x.get("priority", 0),
        ),
    )

    return {
        "tasks": ordered,
        "optimized": True,
    }
