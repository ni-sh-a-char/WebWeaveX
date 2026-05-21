from __future__ import annotations

from typing import Any, Dict, List


def build_control_flow_graph(ast_ir: Dict[str, Any]) -> Dict[str, Any]:

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    funcs = ast_ir.get("functions", [])

    for fn in funcs:
        nodes.append({
            "id": fn["name"],
            "type": "function",
        })

    for i in range(len(funcs) - 1):
        edges.append({
            "from": funcs[i]["name"],
            "to": funcs[i + 1]["name"],
            "relation": "possible_flow",
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
        "deterministic": True,
    }
