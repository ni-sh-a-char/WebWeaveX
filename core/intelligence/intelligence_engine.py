"""Intelligence Engine - Orchestrates all intelligence modules (VALIDATED)."""

from typing import Dict, Any

from core.intelligence.graph_analyzer import analyze_graph
from core.intelligence.centrality_engine import compute_centrality
from core.intelligence.cluster_engine import detect_clusters
from core.intelligence.flow_engine import detect_flows
from core.intelligence.complexity_engine import compute_complexity
from core.intelligence.pattern_engine import detect_patterns


def _validate_intelligence(intel: Dict[str, Any]) -> None:
    """
    Validate intelligence output structure.
    Raises error if invalid.
    """

    required = [
        "analysis",
        "central_nodes",
        "clusters",
        "flows",
        "complexity",
        "patterns"
    ]

    for key in required:
        if key not in intel:
            raise RuntimeError(f"Invalid intelligence output: missing {key}")


def run_intelligence(graph: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run full intelligence pipeline.

    Guarantees:
    - Deterministic output
    - Structural-only analysis
    - Validation enforced
    """

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    analysis = analyze_graph(nodes, edges)
    central = compute_centrality(nodes, edges)
    clusters = detect_clusters(nodes, edges)
    flows = detect_flows(edges)
    complexity = compute_complexity(nodes, edges)
    patterns = detect_patterns(analysis)

    result = {
        "analysis": analysis,
        "central_nodes": central[:5],  # top-k
        "clusters": clusters,
        "flows": flows,
        "complexity": complexity,
        "patterns": patterns
    }

    _validate_intelligence(result)

    return result