from __future__ import annotations

from typing import Any, Dict, List

from core.execution.runtime_worker_engine import build_runtime_workers


def federate_runtime_execution(
    workers: List[Dict[str, Any]],
    actions: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    built = build_runtime_workers(workers)
    routes: List[Dict[str, Any]] = []

    for index, worker in enumerate(built):
        action = (actions or [{}])[index % max(len(actions or [{}]), 1)] if actions else {}
        routes.append({
            "worker_id": worker["worker_id"],
            "runtime": worker["runtime"],
            "action_id": str(action.get("id", f"route:{index}")),
            "route_order": index,
        })

    return {
        "workers": built,
        "execution_routes": sorted(routes, key=lambda item: item["route_order"]),
        "federated": True,
        "bounded": True,
    }
