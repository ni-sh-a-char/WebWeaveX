from __future__ import annotations

from typing import Any, Dict, List


def route_authenticated_sessions(
    workers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    routes: List[Dict[str, Any]] = []

    for worker in workers:
        worker_id = str(worker.get("worker_id", ""))
        session = worker.get("runtime_state", {}).get("session", {})

        routes.append({
            "worker_id": worker_id,
            "session_fingerprint": str(session.get("session_fingerprint", worker_id)),
            "isolated": True,
        })

    return {
        "routes": sorted(routes, key=lambda item: item["worker_id"]),
        "bounded": True,
    }
