from __future__ import annotations

from typing import Any, Dict, List


def route_browser_identity(
    workers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    routes: List[Dict[str, Any]] = []

    for worker in workers:
        identity = worker.get("identity", {})
        routes.append({
            "worker_id": str(worker.get("worker_id", "")),
            "profile_id": str(identity.get("profile_id", "default")),
            "fingerprint_hash": str(identity.get("fingerprint_hash", "")),
        })

    return {
        "routes": sorted(routes, key=lambda item: item["worker_id"]),
        "bounded": True,
    }
