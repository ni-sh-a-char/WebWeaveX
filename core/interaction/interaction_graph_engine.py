from __future__ import annotations

from typing import Any, Dict, List

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload

MAX_GRAPH_NODES = 10000
MAX_GRAPH_EDGES = 50000


def build_interaction_graph(
    interactions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    previous_id = "state_root"
    nodes.append({
        "id": previous_id,
        "type": "state",
        "name": "root",
    })

    for index, interaction in enumerate(interactions[:MAX_GRAPH_NODES]):
        node_id = str(interaction.get("id", f"interaction_{index}"))
        action = str(interaction.get("action", ""))
        selector = str(interaction.get("selector", ""))

        node_type = "form" if action == "fill" else "page"
        if "modal" in selector.lower():
            node_type = "modal"
        if "tab" in selector.lower():
            node_type = "tab"

        nodes.append({
            "id": node_id,
            "type": node_type,
            "action": action,
            "selector": selector,
        })

        relation = action or "transition"
        if action == "click":
            relation = "click"
        elif action in {"fill", "select"}:
            relation = "submission"
        elif action == "wait":
            relation = "navigation"

        edges.append({
            "from": previous_id,
            "to": node_id,
            "relation": relation,
        })

        previous_id = node_id

    graph = {
        "ir": "interaction_graph",
        "nodes": nodes[:MAX_GRAPH_NODES],
        "edges": edges[:MAX_GRAPH_EDGES],
        "graph_hash": compute_kaalka_hash_payload({
            "nodes": nodes[:MAX_GRAPH_NODES],
            "edges": edges[:MAX_GRAPH_EDGES],
        }),
        "bounded": True,
    }

    return graph


def interaction_graph_to_runtime_ir(
    graph: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "interaction_runtime",
        "nodes": list(graph.get("nodes", [])),
        "edges": list(graph.get("edges", [])),
        "bounded": True,
    }
