from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_grpc_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "protocol": "grpc",
        "services": sorted(snap.get("services", []), key=str),
        "methods": sorted(snap.get("methods", []), key=str),
        "schemas": list(snap.get("protobuf", [])),
        "bounded": True,
    }
