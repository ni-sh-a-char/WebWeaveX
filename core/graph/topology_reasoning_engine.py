from __future__ import annotations

from typing import Any, Dict

from core.graph.topology_proof_engine import prove_topology
from core.graph.graph_entropy_engine import model_graph_entropy


def reason_topology(graph: Dict[str, Any]) -> Dict[str, Any]:
    proof = prove_topology(graph)
    entropy = model_graph_entropy(graph)
    return {
        **proof,
        "entropy": entropy.get("entropy", 0),
        "evidence": ["graph:topology_proof"],
        "justification": {"hubs": proof.get("hubs", []), "max_degree": proof.get("max_degree", 0)},
        "uncertainty": {"visible": entropy.get("entropy", 0) > 0},
        "deterministic_inputs": proof.get("deterministic_inputs", []),
    }
