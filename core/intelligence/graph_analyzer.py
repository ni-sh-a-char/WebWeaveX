"""Graph Analyzer - Structural analysis only (SAFE + DETERMINISTIC)."""

from typing import List, Dict, Any


def analyze_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze graph structure.

    Guarantees:
    - Safe node handling
    - Deterministic output
    """

    n = len(nodes)
    e = len(edges)

    density = 0.0
    if n > 1:
        density = e / (n * (n - 1))

    degree = {}

    # SAFE initialization (fixed)
    for node in nodes:
        node_id = node.get("id", "")
        if node_id:
            degree[node_id] = 0

    # Degree counting
    for edge in edges:
        f = edge.get("from", "")
        t = edge.get("to", "")

        if f in degree:
            degree[f] += 1
        if t in degree:
            degree[t] += 1

    return {
        "node_count": n,
        "edge_count": e,
        "density": density,
        "degree_map": dict(sorted(degree.items()))
    }