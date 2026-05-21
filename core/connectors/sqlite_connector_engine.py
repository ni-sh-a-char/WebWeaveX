from __future__ import annotations

from typing import Any, Dict, Optional


def extract_sqlite_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "database_type": "sqlite",
        "schemas": ["main"],
        "tables": sorted(snap.get("tables", []), key=str),
        "indexes": list(snap.get("indexes", [])),
        "metrics": dict(snap.get("metrics", {})),
        "active_connections": 1,
        "replication_state": "local",
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
