from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_state_graph(
    snapshot: Dict[str, Any],
    delta: Dict[str, Any],
    convergence: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    snapshot_id = str(snapshot.get("snapshot_id", "snapshot:0"))
    nodes.append({"id": snapshot_id, "type": "snapshot"})

    delta_id = str(delta.get("delta_id", "delta:0"))
    nodes.append({"id": delta_id, "type": "delta"})
    edges.append({
        "from": snapshot_id,
        "to": delta_id,
        "relation": "mutates",
    })

    for change in delta.get("changes", [])[:5000]:
        node_id = f"change:{change.get('field', '')}"
        nodes.append({"id": node_id, "type": "mutation"})
        edges.append({
            "from": delta_id,
            "to": node_id,
            "relation": "propagates",
        })

    converged_id = "convergence:root"
    nodes.append({"id": converged_id, "type": "convergence"})
    edges.append({
        "from": delta_id,
        "to": converged_id,
        "relation": "converges",
    })

    if delta.get("changes"):
        edges.append({
            "from": converged_id,
            "to": snapshot_id,
            "relation": "synchronizes",
        })

    nodes.append({"id": "checkpoint:sync", "type": "checkpoint"})
    edges.append({
        "from": converged_id,
        "to": "checkpoint:sync",
        "relation": "restores",
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
