from __future__ import annotations

from typing import Any, Dict, List

MAX_NODES = 10000


def build_runtime_topology(
    services: Dict[str, Any],
    infra: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for svc in services.get("services", []):
        nodes.append({
            "id": svc["file"],
            "type": "service",
        })

    for item in infra.get("infra", []):
        nodes.append({
            "id": item["file"],
            "type": item["type"],
        })

        edges.append({
            "from": item["file"],
            "to": item["type"],
            "relation": "infra_signal",
        })

    return {
        "nodes": sorted(
            nodes,
            key=lambda x: x["id"],
        )[:MAX_NODES],
        "edges": sorted(
            edges,
            key=lambda x: (
                str(x.get("from")),
                str(x.get("to")),
            ),
        ),
        "bounded": True,
    }
