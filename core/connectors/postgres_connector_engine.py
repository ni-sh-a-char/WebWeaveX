from __future__ import annotations

from typing import Any, Dict, Optional


def extract_postgres_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "database_type": "postgresql",
        "schemas": list(snap.get("schemas", ["public"])),
        "tables": sorted(snap.get("tables", []), key=str),
        "indexes": list(snap.get("indexes", [])),
        "metrics": dict(snap.get("metrics", {})),
        "active_connections": int(snap.get("active_connections", 0)),
        "replication_state": str(snap.get("replication_state", "unknown")),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
