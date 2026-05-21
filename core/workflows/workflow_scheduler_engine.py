from __future__ import annotations

from typing import Any, Dict, List


def schedule_workflow_execution(
    plans: List[Dict[str, Any]],
    tick: int = 0,
) -> Dict[str, Any]:
    ordered = sorted(
        plans,
        key=lambda item: (
            int(item.get("priority", item.get("objective_priority", 0))),
            str(item.get("objective", "")),
        ),
    )

    schedule: List[Dict[str, Any]] = []
    for index, plan in enumerate(ordered[:10000]):
        schedule.append({
            "objective": plan.get("objective", ""),
            "priority": int(plan.get("priority", 0)),
            "tick": tick + index,
            "pacing": index,
            "retries": 0,
            "distributed_order": index,
        })

    return {
        "schedule": schedule,
        "count": len(schedule),
        "bounded": True,
    }
