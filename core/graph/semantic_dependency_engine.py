from __future__ import annotations

from typing import Any, Dict

from core.evidence import structure_cognition
from core.parsers import parse_source


def reconstruct_graph_dependencies(text: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(text or "", path=path)
    graph = parsed.get("semantic_graph", {}) or {}
    edges = graph.get("edges", []) or []
    deps = [
        {"from": e.get("from"), "to": e.get("to"), "basis": (e.get("metadata") or {}).get("edge_basis", "observed")}
        for e in edges
        if isinstance(e, dict) and e.get("from") and e.get("to")
    ]
    observed = {"nodes": len(graph.get("nodes", []) or [])}
    inferred = {"graph_dependencies": deps}
    reconciled = {"dependencies": deps}
    return structure_cognition(observed, inferred, reconciled, parsed=parsed)
