from __future__ import annotations

from typing import Any, Dict, List


MAX_GRAPH_EDGES = 100000


def build_distributed_causal_graph(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    causality = runtime_ir.get("runtime_causality_graph", {})
    propagation = runtime_ir.get("distributed_propagation", {})
    causal_edges: List[Dict[str, Any]] = []
    for edge in causality.get("edges", [])[:MAX_GRAPH_EDGES]:
        causal_edges.append(
            {
                "from": edge.get("from"),
                "to": edge.get("to"),
                "relation": "execution_causes",
            }
        )
    for path in propagation.get("propagation_paths", [])[:MAX_GRAPH_EDGES]:
        causal_edges.append(
            {
                "from": path.get("source"),
                "to": path.get("target"),
                "relation": "propagates",
            }
        )
    causal_edges = sorted(
        causal_edges,
        key=lambda x: (str(x.get("from")), str(x.get("to"))),
    )[:MAX_GRAPH_EDGES]
    return {
        "causal_edges": causal_edges,
        "edge_count": len(causal_edges),
        "bounded": True,
    }
