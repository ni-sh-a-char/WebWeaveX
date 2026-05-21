from __future__ import annotations

from typing import Any, Dict, List


def schedule_semantic_dependencies(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        tasks,
        key=lambda x: str(
            x.get("id")
        ),
    )

    return {
        "schedule": ordered,
        "count": len(ordered),
    }
