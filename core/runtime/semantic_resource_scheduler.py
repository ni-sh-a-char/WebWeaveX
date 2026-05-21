from __future__ import annotations

from typing import Any, Dict, List


def schedule_semantic_resources(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        tasks,
        key=lambda x: str(x.get("priority", 0)),
    )

    return {
        "scheduled": ordered,
        "count": len(ordered),
    }
