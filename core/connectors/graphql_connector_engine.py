from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_graphql_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "protocol": "graphql",
        "endpoints": list(snap.get("endpoints", ["/graphql"])),
        "schemas": list(snap.get("schemas", [])),
        "types": sorted(snap.get("types", []), key=str),
        "bounded": True,
    }
