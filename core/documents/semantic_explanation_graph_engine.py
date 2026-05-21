from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_causality_engine import reconstruct_semantic_causality
from core.evidence import structure_cognition


def build_explanation_graph(text: str) -> Dict[str, Any]:
    causality = reconstruct_semantic_causality(text)
    edges: List[Dict[str, Any]] = causality.get("reconciled", {}).get("what_explains_what", [])
    nodes = sorted({e.get("from") for e in edges} | {e.get("to") for e in edges})
    graph = {
        "nodes": [{"id": n, "kind": "concept", "metadata": {}} for n in nodes if n],
        "edges": [{"from": e["from"], "to": e["to"], "metadata": {"relation": "explains"}} for e in edges],
        "max_edges": 5000,
    }
    observed = {"node_count": len(nodes)}
    inferred = {"explanation_graph": graph}
    reconciled = graph
    return structure_cognition(observed, inferred, reconciled, parsed=None)
