from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


MAX_WORKERS = 128


def assign_distributed_workers(
    tasks: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    assignments = []

    worker_id = 0

    for task in tasks:

        assignments.append({
            "worker": worker_id,
            "task": task,
        })

        worker_id = (
            worker_id + 1
        ) % MAX_WORKERS

    return {
        "assignments": assignments,
        "workers_used": min(
            len(tasks),
            MAX_WORKERS,
        ),
    }
