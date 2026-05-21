from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_evolution_graph(
    evolution: Dict[str, Any],
    repairs: Dict[str, Any],
    optimization: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    evolution_id = str(evolution.get("evolution_id", "evolution:root"))
    nodes.append({"id": evolution_id, "type": "evolution"})

    for mutation in evolution.get("mutations", [])[:5000]:
        node_id = f"mutation:{mutation.get('kind')}:{mutation.get('target')}"
        nodes.append({"id": node_id, "type": "mutation"})
        edges.append({
            "from": evolution_id,
            "to": node_id,
            "relation": "evolves",
        })

    for repair in repairs.get("repairs", [])[:5000]:
        node_id = f"repair:{repair.get('action', '')}"
        nodes.append({"id": node_id, "type": "repair"})
        edges.append({
            "from": node_id,
            "to": evolution_id,
            "relation": "repairs",
        })

    opt_id = "optimization:root"
    nodes.append({"id": opt_id, "type": "optimization"})
    edges.append({
        "from": opt_id,
        "to": evolution_id,
        "relation": "optimizes",
    })

    edges.append({
        "from": evolution_id,
        "to": evolution_id,
        "relation": "converges",
    })

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (
                item.get("from", ""),
                item.get("to", ""),
                item.get("relation", ""),
            ),
        ),
        "bounded": True,
    }
