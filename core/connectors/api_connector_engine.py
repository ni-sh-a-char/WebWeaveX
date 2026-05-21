from __future__ import annotations

from typing import Any, Dict, Optional

from core.connectors.graphql_connector_engine import extract_graphql_runtime
from core.connectors.grpc_connector_engine import extract_grpc_runtime


def extract_api_runtime(
    api_type: str = "rest",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    normalized = api_type.lower()

    base = {
        "api_type": normalized,
        "endpoints": sorted(snap.get("endpoints", []), key=str),
        "schemas": list(snap.get("schemas", [])),
        "auth_state": dict(snap.get("auth", {})),
        "rate_limits": dict(snap.get("rate_limits", {})),
        "response_topology": list(snap.get("responses", [])),
        "pagination_models": list(snap.get("pagination", [])),
        "bounded": True,
    }

    if normalized == "graphql":
        base["graphql"] = extract_graphql_runtime(snap.get("graphql"))
    elif normalized == "grpc":
        base["grpc"] = extract_grpc_runtime(snap.get("grpc"))

    return base
