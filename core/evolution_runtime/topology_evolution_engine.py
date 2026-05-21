from __future__ import annotations

from typing import Any, Dict, List, Optional


def evolve_runtime_topology(
    workers: Optional[List[Dict[str, Any]]] = None,
    sync: Optional[Dict[str, Any]] = None,
    causality: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    workers = workers or []
    worker_ids = sorted(
        str(w.get("worker_id", w.get("id", f"w:{index}")))
        for index, w in enumerate(workers)
    )

    return {
        "worker_routing": worker_ids,
        "sync_paths": ["browser", "native", "distributed"],
        "causality_propagation": bool(causality),
        "workflow_routing": ["primary", "distributed"],
        "federation": len(worker_ids),
        "bounded": True,
    }
