from __future__ import annotations

from typing import Any, Dict, List


def build_distributed_topology(
    services: List[str],
) -> Dict[str, Any]:

    nodes = []
    edges = []

    for svc in services:

        nodes.append({
            "id": svc,
            "type": "service",
        })

    for i in range(len(services) - 1):

        edges.append({
            "from": services[i],
            "to": services[i + 1],
            "relation": "distributed_dependency",
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
