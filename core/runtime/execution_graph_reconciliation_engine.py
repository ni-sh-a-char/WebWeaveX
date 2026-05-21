from __future__ import annotations

from typing import Any, Dict, List


def reconcile_execution_graphs(
    runtime_graph: Dict[str, Any],
    topology_graph: Dict[str, Any],
) -> Dict[str, Any]:

    runtime_nodes = {
        n["id"]
        for n in runtime_graph.get("nodes", [])
    }

    topology_nodes = {
        n["id"]
        for n in topology_graph.get("nodes", [])
    }

    overlap = sorted(
        runtime_nodes & topology_nodes
    )

    return {
        "shared_nodes": overlap,
        "runtime_only": sorted(
            runtime_nodes - topology_nodes
        ),
        "topology_only": sorted(
            topology_nodes - runtime_nodes
        ),
        "consistent": len(overlap) > 0,
    }
