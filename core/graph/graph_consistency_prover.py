from __future__ import annotations

from typing import Any, Dict

from core.graph.graph_consistency_engine import assess_graph_consistency
from core.graph.semantic_graph_validator import validate_semantic_graph


def prove_graph_consistency(graph: Dict[str, Any]) -> Dict[str, Any]:
    validation = validate_semantic_graph(graph)
    consistency = assess_graph_consistency(graph)
    proved = validation["valid"] and consistency["consistent"]
    return {
        "proved": proved,
        "validation": validation,
        "consistency": consistency,
        "deterministic_inputs": validation.get("deterministic_inputs", []),
    }
