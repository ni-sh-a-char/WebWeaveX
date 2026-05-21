from __future__ import annotations

from typing import Any, Dict, List


def build_execution_plan(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        tasks,
        key=lambda x: x.get("priority", 0),
    )

    return {
        "plan": ordered,
        "task_count": len(ordered),
        "deterministic": True,
    }
