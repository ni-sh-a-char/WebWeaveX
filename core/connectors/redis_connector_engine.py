from __future__ import annotations

from typing import Any, Dict, Optional


def extract_redis_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "database_type": "redis",
        "schemas": [],
        "tables": list(snap.get("keys", []))[:1000],
        "indexes": [],
        "metrics": dict(snap.get("metrics", {})),
        "active_connections": int(snap.get("clients", 0)),
        "replication_state": str(snap.get("role", "master")),
        "streams": list(snap.get("streams", [])),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
