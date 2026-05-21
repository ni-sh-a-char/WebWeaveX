from __future__ import annotations

from typing import Any, Dict


def align_runtime_phases(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    workers = len(
        list(runtime_ir.get("distributed_workers", []) or [])
    )
    tasks = len(list(runtime_ir.get("tasks", []) or []))
    aligned = workers == 0 or tasks <= workers
    return {
        "phase_aligned": aligned,
        "worker_count": workers,
        "task_count": tasks,
    }
