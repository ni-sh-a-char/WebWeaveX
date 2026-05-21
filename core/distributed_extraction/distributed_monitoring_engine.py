from __future__ import annotations

from typing import Any, Dict, List


def monitor_extraction_cluster(
    workers: List[Dict[str, Any]],
    queue: List[Dict[str, Any]],
) -> Dict[str, Any]:
    statuses: Dict[str, int] = {}

    for worker in workers:
        status = str(worker.get("status", "unknown"))
        statuses[status] = statuses.get(status, 0) + 1

    return {
        "worker_statuses": dict(sorted(statuses.items())),
        "queue_depth": len(queue),
        "active_workers": statuses.get("idle", 0) + statuses.get("running", 0),
        "bounded": True,
    }
