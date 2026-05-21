from __future__ import annotations

from typing import Any, Dict, List


MAX_CAUSAL_EDGES = 100000


def build_semantic_causality_graph(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = list(
        runtime_ir.get(
            "transitions",
            [],
        )
    )

    edges: List[Dict[str, Any]] = []

    for transition in transitions[:MAX_CAUSAL_EDGES]:

        source = str(
            transition.get(
                "from",
                "unknown",
            )
        )

        target = str(
            transition.get(
                "to",
                "unknown",
            )
        )

        edges.append(
            {
                "from": source,
                "to": target,
                "relation": "causes",
            }
        )

    node_set = {
        edge["from"] for edge in edges
    }.union(
        {edge["to"] for edge in edges}
    )

    return {
        "nodes": sorted(node_set)[:MAX_CAUSAL_EDGES],
        "edges": sorted(
            edges,
            key=lambda x: (
                x["from"],
                x["to"],
            ),
        )[:MAX_CAUSAL_EDGES],
        "bounded": True,
    }
