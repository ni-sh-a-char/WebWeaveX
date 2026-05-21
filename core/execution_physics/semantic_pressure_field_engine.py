from __future__ import annotations

from typing import Any, Dict, List


MAX_FIELD = 1000


def build_pressure_field(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    workers_raw = runtime_ir.get(
        "distributed_workers",
        [],
    )
    if isinstance(workers_raw, dict):
        workers = list(workers_raw.get("assignments", []))
    else:
        workers = list(workers_raw)

    field = []

    for worker in workers[:MAX_FIELD]:
        worker_key = (
            str(worker.get("worker"))
            if isinstance(worker, dict)
            else str(worker)
        )
        field.append(
            {
                "worker": worker_key,
                "pressure": 1,
            }
        )

    return {
        "pressure_field": sorted(
            field,
            key=lambda x: x["worker"],
        ),
        "bounded": True,
    }
