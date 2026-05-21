from __future__ import annotations

from typing import Any, Dict, List

from core.distributed_extraction.extraction_worker_engine import create_extraction_worker


def recover_distributed_runtime(
    checkpoint: Dict[str, Any],
    failed_worker_ids: List[str] | None = None,
) -> Dict[str, Any]:
    failed = set(failed_worker_ids or [])
    workers = list(checkpoint.get("workers", []))
    queue = list(checkpoint.get("queue", []))
    recovered_workers: List[Dict[str, Any]] = []

    for worker in workers:
        worker_id = str(worker.get("worker_id", ""))

        if worker_id in failed:
            recovered_workers.append(
                create_extraction_worker(
                    worker_id=worker_id,
                    runtime_state=worker.get("runtime_state", {}),
                    identity=worker.get("identity", {}),
                    adaptive_runtime=worker.get("adaptive_runtime", {}),
                    stream_runtime=worker.get("stream_runtime", {}),
                    status="recovered",
                )
            )
        else:
            recovered_workers.append(worker)

    return {
        "workers": recovered_workers,
        "queue": queue,
        "runtime_graph": checkpoint.get("runtime_graph", {}),
        "stream_runtime": checkpoint.get("stream_runtime", {}),
        "adaptive_memory": checkpoint.get("adaptive_memory", {}),
        "recovered": True,
        "bounded": True,
    }
