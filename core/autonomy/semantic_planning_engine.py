from __future__ import annotations

from typing import Any, Dict, List

from .semantic_goal_engine import resolve_semantic_goal
from .semantic_task_decomposition_engine import decompose_semantic_task


MAX_PLAN_STEPS = 1000


def plan_semantic_autonomy(
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    goal = resolve_semantic_goal(payload)
    decomposition = decompose_semantic_task(goal)
    steps = [
        {
            "step": idx,
            "action": subtask.get("semantic_unit"),
            "task_id": subtask.get("id"),
        }
        for idx, subtask in enumerate(
            decomposition.get("subtasks", [])[:MAX_PLAN_STEPS]
        )
    ]
    return {
        "goal": goal,
        "steps": steps,
        "step_count": len(steps),
        "bounded": True,
    }
