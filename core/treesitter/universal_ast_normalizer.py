from __future__ import annotations

from typing import Any, Dict, List


MAX_AST_NODES = 10000


def normalize_ast(
    raw_nodes: List[Dict[str, Any]],
    language: str,
) -> Dict[str, Any]:

    nodes = []

    edges = []

    for i, node in enumerate(
        raw_nodes[:MAX_AST_NODES]
    ):

        node_id = f"{language}_{i}"

        nodes.append({
            "id": node_id,
            "type": node.get("type"),
            "language": language,
        })

        parent = node.get("parent")

        if parent is not None:

            edges.append({
                "from": parent,
                "to": node_id,
                "relation": "ast_edge",
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "language": language,
        "bounded": True,
    }
