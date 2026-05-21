from __future__ import annotations

from typing import Any, Dict

from core.graph.graph_invariant_engine import check_graph_invariants


def validate_semantic_topology(graph: Dict[str, Any]) -> Dict[str, Any]:
    inv = check_graph_invariants(graph)
    edges = graph.get("edges", []) or []
    grounded = sum(1 for e in edges if isinstance(e, dict) and e.get("evidence"))
    return {
        **inv,
        "grounded_edges": grounded,
        "topology_valid": inv["valid"] and grounded == len(edges),
    }
