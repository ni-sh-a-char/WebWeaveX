from __future__ import annotations

from typing import Any, Dict

from core.graph.semantic_dependency_engine import reconstruct_graph_dependencies
from core.evidence import structure_cognition


def reconstruct_graph_causality(text: str, path: str = "") -> Dict[str, Any]:
    deps = reconstruct_graph_dependencies(text, path=path)
    edges = deps.get("reconciled", {}).get("dependencies", [])
    causal = [
        {**e, "relation": "depends_on", "evidence": ["graph:dependency"], "lineage": {"stage": "graph_causality"}}
        for e in edges
        if isinstance(e, dict)
    ]
    observed = deps.get("observed", {})
    inferred = {"causal_edges": causal}
    reconciled = {"graph_causality": causal}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
