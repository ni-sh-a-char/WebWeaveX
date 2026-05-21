from __future__ import annotations

from typing import Any, Dict


MAX_HEALTH_NODES = 10000


def build_runtime_health_graph(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    nodes = topology.get(
        "nodes",
        [],
    )

    health_nodes = []

    for node in nodes[:MAX_HEALTH_NODES]:

        health_nodes.append(
            {
                "id": node.get("id"),
                "status": "healthy",
            }
        )

    return {
        "health_nodes": health_nodes,
        "bounded": True,
    }
