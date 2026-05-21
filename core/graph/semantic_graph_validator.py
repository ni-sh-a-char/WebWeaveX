from __future__ import annotations

from typing import Any, Dict

from core.graph.graph_invariant_engine import check_graph_invariants
from core.graph.semantic_edge_validation_engine import validate_semantic_edge


def validate_semantic_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    inv = check_graph_invariants(graph)
    edge_results = [validate_semantic_edge(e) for e in graph.get("edges", []) if isinstance(e, dict)]
    invalid = [i for i, r in enumerate(edge_results) if not r.get("valid")]
    return {
        "valid": inv["valid"] and not invalid,
        "invariants": inv,
        "invalid_edges": invalid,
        "edge_count": len(edge_results),
        "deterministic_inputs": inv.get("deterministic_inputs", []),
    }
