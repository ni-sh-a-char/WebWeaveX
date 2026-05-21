from __future__ import annotations

from typing import Any, Dict, List


MAX_TASKS = 1000


def decompose_semantic_task(
    task: Dict[str, Any],
) -> Dict[str, Any]:

    goal = str(
        task.get("goal", "")
    )

    words = [
        w.strip()
        for w in goal.split()
        if w.strip()
    ]

    subtasks = []

    for idx, word in enumerate(
        words[:MAX_TASKS]
    ):

        subtasks.append(
            {
                "id": f"task_{idx}",
                "semantic_unit": word,
            }
        )

    return {
        "subtasks": subtasks,
        "count": len(subtasks),
        "bounded": True,
    }
