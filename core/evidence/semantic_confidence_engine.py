from __future__ import annotations

from typing import Any, Dict, List, Optional


def score_semantic_confidence(
    parsed: Optional[Dict[str, Any]] = None,
    graph: Optional[Dict[str, Any]] = None,
    extra_evidence: Optional[List[str]] = None,
) -> Dict[str, Any]:
    inputs: List[str] = []
    evidence: List[str] = []
    score = 0.2
    if isinstance(parsed, dict):
        flags = parsed.get("evidence", {})
        if isinstance(flags, dict):
            for key, val in sorted(flags.items()):
                inputs.append(f"parser.{key}={bool(val)}")
                if val:
                    evidence.append(f"parser:{key}")
                    score += 0.12
    if isinstance(graph, dict):
        nodes = graph.get("nodes", []) or []
        edges = graph.get("edges", []) or []
        inputs.append(f"graph.nodes={len(nodes)}")
        inputs.append(f"graph.edges={len(edges)}")
        if edges:
            evidence.append("graph:edges")
            score += min(0.25, len(edges) * 0.01)
    for e in extra_evidence or []:
        evidence.append(str(e))
        score += 0.05
    score = round(min(1.0, max(0.0, score)), 3)
    return {
        "score": score,
        "basis": {
            "parser_density": len([e for e in evidence if e.startswith("parser:")]),
            "graph_edges": len((graph or {}).get("edges", []) or []) if graph else 0,
        },
        "evidence": sorted(set(evidence)),
        "deterministic_inputs": sorted(inputs),
    }
