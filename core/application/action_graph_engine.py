from __future__ import annotations

from typing import Any, Dict, List


def build_action_graph(
    interactions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for index, action in enumerate(interactions[:10000]):
        action_type = str(
            action.get("action", action.get("type", "action"))
        )
        selector = str(action.get("selector", ""))

        node_id = f"action_{index}"
        nodes.append({
            "id": node_id,
            "type": action_type,
            "selector": selector,
        })

        if index > 0:
            edges.append({
                "from": f"action_{index - 1}",
                "to": node_id,
                "relation": "sequential",
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
