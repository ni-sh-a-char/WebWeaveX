from __future__ import annotations

from typing import Any, Dict, List

from core.distributed_extraction.distributed_load_balancer import (
    balance_extraction_workloads,
)
from core.distributed_extraction.distributed_recovery_engine import (
    recover_distributed_runtime,
)
from core.distributed_extraction.extraction_worker_engine import (
    create_extraction_worker,
)


def failover_extraction_runtime(
    checkpoint: Dict[str, Any],
    dead_worker_id: str,
) -> Dict[str, Any]:
    workers = list(checkpoint.get("workers", []))
    tasks = list(checkpoint.get("queue", []))

    surviving = [
        worker for worker in workers
        if str(worker.get("worker_id", "")) != dead_worker_id
    ]

    replacement = create_extraction_worker(
        worker_id=f"{dead_worker_id}_migrated",
        runtime_state={},
        identity={},
        adaptive_runtime={},
        stream_runtime={},
        status="migrated",
    )

    surviving.append(replacement)

    recovered = recover_distributed_runtime(
        checkpoint,
        failed_worker_ids=[dead_worker_id],
    )

    assignments = balance_extraction_workloads(surviving, tasks)

    return {
        "dead_worker": dead_worker_id,
        "replacement_worker": replacement["worker_id"],
        "assignments": assignments.get("assignments", []),
        "recovered": recovered,
        "bounded": True,
    }
