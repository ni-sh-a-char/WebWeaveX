from __future__ import annotations

from typing import Any, Dict, List, Optional


_CONNECTOR_KINDS = (
    "database",
    "api",
    "kubernetes",
    "docker",
    "telemetry",
    "ide",
    "cicd",
)


def reconstruct_connector_runtime(
    connectors: Optional[List[Dict[str, Any]]] = None,
    live_ir: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    connectors = connectors or []
    live_ir = live_ir or {}

    rebuilt: List[Dict[str, Any]] = []
    for index, connector in enumerate(connectors[:1000]):
        kind = str(connector.get("kind", connector.get("type", "api")))
        if kind not in _CONNECTOR_KINDS:
            kind = "api"
        rebuilt.append({
            "id": str(connector.get("id", f"connector:{index}")),
            "kind": kind,
            "state": dict(connector.get("state", {})),
            "reconstructed": True,
        })

    streams = live_ir.get("streams", live_ir.get("connectors", []))
    if isinstance(streams, dict):
        streams = streams.get("streams", [])

    return {
        "connectors": sorted(rebuilt, key=lambda item: item["id"]),
        "streams": list(streams)[:1000] if isinstance(streams, list) else [],
        "bounded": True,
    }
