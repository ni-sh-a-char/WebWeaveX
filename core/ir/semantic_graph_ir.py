from __future__ import annotations

from typing import Any, Dict

from core.graph.graph_consistency_prover import prove_graph_consistency
from core.ir._base import empty_confidence, empty_lineage

SemanticGraphIR = Dict[str, Any]


def compile_semantic_graph_ir(graph: Dict[str, Any]) -> SemanticGraphIR:
    proof = prove_graph_consistency(graph)
    return {
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
        "proof": proof,
        "lineage": empty_lineage("semantic_graph_ir"),
        "confidence": {"score": 1.0 if proof.get("proved") else 0.3, "basis": proof.get("deterministic_inputs", []), "deterministic": True},
    }
