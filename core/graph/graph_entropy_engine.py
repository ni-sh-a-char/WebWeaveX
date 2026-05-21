from __future__ import annotations

from typing import Any, Dict


def model_graph_entropy(graph: Dict[str, Any]) -> Dict[str, Any]:
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    kinds = {n.get("kind") for n in nodes if isinstance(n, dict)}
    entropy = round(min(1.0, len(nodes) * 0.02 + len(edges) * 0.03 + len(kinds) * 0.05), 3)
    return {"entropy": entropy, "kind_diversity": len(kinds), "deterministic_inputs": [f"H={entropy}"]}
