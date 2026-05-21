from __future__ import annotations

from typing import Any, Dict


MAX_FORCE = 100000


def compute_scheduler_force(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    tasks = len(list(runtime_ir.get("tasks", []) or []))
    workers = max(
        len(list(runtime_ir.get("distributed_workers", []) or [])),
        1,
    )
    force = min(tasks * workers, MAX_FORCE)
    return {
        "scheduler_force": force,
        "task_count": tasks,
        "bounded": True,
    }
