from __future__ import annotations

from typing import Any, Dict


MAX_GOAL_SIZE = 4096


def resolve_semantic_goal(
    payload: Dict[str, Any],
) -> Dict[str, Any]:

    goal = str(
        payload.get("goal", "")
    )[:MAX_GOAL_SIZE]

    return {
        "goal": goal,
        "resolved": bool(goal),
        "priority": int(
            payload.get("priority", 1)
        ),
    }
