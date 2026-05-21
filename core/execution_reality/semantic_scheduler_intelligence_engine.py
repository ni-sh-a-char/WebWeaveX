from __future__ import annotations

from typing import Any, Dict


MAX_SCHEDULED = 1000


def analyze_scheduler_intelligence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    tasks = runtime_ir.get(
        "tasks",
        [],
    )

    ordered = sorted(
        tasks,
        key=lambda x: (
            x.get(
                "priority",
                0,
            ),
            str(
                x.get("id")
            ),
        ),
    )

    return {
        "scheduled_tasks": ordered[:MAX_SCHEDULED],
        "bounded": True,
    }
