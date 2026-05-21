from __future__ import annotations

from typing import Any, Dict


MAX_SCHEDULING_PRESSURE = 100000


def compute_scheduling_pressure(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    tasks = list(runtime_ir.get("tasks", []) or [])
    workers = list(
        runtime_ir.get("distributed_workers", []) or []
    )
    pressure = min(
        len(tasks) * max(len(workers), 1),
        MAX_SCHEDULING_PRESSURE,
    )
    return {
        "scheduling_pressure": pressure,
        "task_count": len(tasks),
        "bounded": True,
    }
