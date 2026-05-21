from __future__ import annotations

from typing import Any, Dict, List


def build_cluster_state(
    workers: List[Dict[str, Any]],
    queue: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "worker_count": len(workers),
        "queue_depth": len(queue),
        "worker_ids": sorted(
            str(worker.get("worker_id", ""))
            for worker in workers
        ),
        "bounded": True,
    }
