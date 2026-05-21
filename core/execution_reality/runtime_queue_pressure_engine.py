from __future__ import annotations

from typing import Any, Dict


MAX_QUEUE_PRESSURE = 100000


def measure_queue_pressure(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    tasks = list(runtime_ir.get("tasks", []) or [])
    workers = list(
        runtime_ir.get("distributed_workers", []) or []
    )
    queue_depth = len(tasks)
    worker_count = max(len(workers), 1)
    pressure = min(
        queue_depth * worker_count,
        MAX_QUEUE_PRESSURE,
    )
    return {
        "queue_depth": queue_depth,
        "queue_pressure": pressure,
        "bounded": True,
    }
