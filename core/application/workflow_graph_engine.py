from __future__ import annotations

from typing import Any, Dict, List


def build_workflow_graph(
    states: List[Dict[str, Any]],
    transitions: List[Dict[str, Any]],
    actions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for index, state in enumerate(states[:5000]):
        route = str(state.get("route", f"state_{index}"))
        nodes.append({
            "id": route,
            "type": "page",
        })

    for transition in transitions[:10000]:
        edges.append({
            "from": str(transition.get("from", "")),
            "to": str(transition.get("to", "")),
            "relation": str(transition.get("relation", "transition")),
        })

    for action in actions[:10000]:
        action_type = str(action.get("action", action.get("type", "")))
        relation = "submit"
        if action_type == "click":
            relation = "navigate"
        elif "modal" in action_type:
            relation = "open_modal"

        edges.append({
            "from": str(action.get("from", "")),
            "to": str(action.get("to", "")),
            "relation": relation,
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
