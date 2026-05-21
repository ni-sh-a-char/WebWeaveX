from __future__ import annotations

from typing import Any, Dict, List

MAX_SCHEDULED = 5000
DEFAULT_COOLDOWN = 5


def schedule_extraction_runtime(
    tasks: List[Dict[str, Any]],
    tick: int = 0,
) -> Dict[str, Any]:
    scheduled: List[Dict[str, Any]] = []

    for index, task in enumerate(tasks[:MAX_SCHEDULED]):
        priority = int(task.get("priority", 0))
        retries = int(task.get("retries", 0))
        cooldown = int(task.get("cooldown", DEFAULT_COOLDOWN))
        pacing = int(task.get("pacing", 1))

        run_at = tick + (cooldown * retries) + (pacing * index)

        scheduled.append({
            "task_id": str(task.get("task_id", f"task_{index}")),
            "url": str(task.get("url", "")),
            "priority": priority,
            "run_at": run_at,
            "retries": retries,
            "bounded": True,
        })

    scheduled = sorted(
        scheduled,
        key=lambda item: (
            int(item.get("run_at", 0)),
            -int(item.get("priority", 0)),
            str(item.get("task_id", "")),
        ),
    )

    return {
        "scheduled": scheduled,
        "tick": tick,
        "bounded": True,
    }
