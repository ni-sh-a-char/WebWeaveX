from __future__ import annotations

from typing import Any, Dict


def balance_runtime_load(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    workers_raw = runtime_ir.get(
        "distributed_workers",
        [],
    )
    if isinstance(workers_raw, dict):
        workers = list(
            workers_raw.get("assignments", [])
        )
    else:
        workers = list(workers_raw)

    assignments = {}

    for idx, worker in enumerate(
        workers
    ):
        if isinstance(worker, dict):
            worker_id = str(
                worker.get("worker")
                or worker.get("id")
                or idx
            )
        else:
            worker_id = str(worker)
        assignments[worker_id] = idx

    return {
        "assignments": dict(
            sorted(assignments.items())
        ),
    }
