from __future__ import annotations

from typing import Any, Dict, List


MAX_CASCADE = 10000


def analyze_dependency_cascade(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = runtime_ir.get("runtime_causality_graph", {})
    edges = list(graph.get("edges", []))[:MAX_CASCADE]
    cascade = [
        {
            "from": edge.get("from"),
            "to": edge.get("to"),
            "depth": idx,
        }
        for idx, edge in enumerate(edges)
    ]
    return {
        "cascade": cascade,
        "cascade_length": len(cascade),
        "bounded": True,
    }
