from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_distributed_causality(
    distributed_result: Optional[Dict[str, Any]] = None,
    worker_events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    distributed_result = distributed_result or {}
    worker_events = list(worker_events or [])

    workers = list(distributed_result.get("workers", []))
    chains: List[Dict[str, Any]] = []

    for index, event in enumerate(worker_events[:10000]):
        chains.append({
            "worker_id": str(event.get("worker_id", f"worker_{index}")),
            "event_id": str(event.get("id", f"dist:{index}")),
            "step": index,
            "relation": "cluster_sync",
        })

    return {
        "worker_causality": chains,
        "autonomous_propagation": distributed_result.get("autonomous", False),
        "remote_chains": list(distributed_result.get("tasks", []))[:1000],
        "cluster_synchronization": {
            "worker_count": len(workers),
            "synced": bool(workers),
        },
        "bounded": True,
    }
