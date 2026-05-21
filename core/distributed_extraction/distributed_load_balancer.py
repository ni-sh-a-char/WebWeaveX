from __future__ import annotations

from typing import Any, Dict, List

MAX_WORKERS = 1000


def balance_extraction_workloads(
    workers: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:
    assignments: List[Dict[str, Any]] = []

    if not workers:
        return {
            "assignments": [],
            "bounded": True,
        }

    active_workers = sorted(
        workers[:MAX_WORKERS],
        key=lambda item: str(item.get("worker_id", "")),
    )

    for index, task in enumerate(tasks):
        worker = active_workers[index % len(active_workers)]
        assignments.append({
            "task_id": str(task.get("task_id", f"task_{index}")),
            "worker_id": str(worker.get("worker_id", "")),
            "partition": index % len(active_workers),
        })

    return {
        "assignments": sorted(
            assignments,
            key=lambda item: (
                str(item.get("worker_id", "")),
                str(item.get("task_id", "")),
            ),
        ),
        "bounded": True,
    }
