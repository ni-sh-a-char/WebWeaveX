from __future__ import annotations

from typing import Any, Dict, List


MAX_LOWERED_EDGES = 10000


def lower_semantic_ir(ir: Dict[str, Any]) -> Dict[str, Any]:
    edges: List[Dict[str, Any]] = list(ir.get("edges", []))[:MAX_LOWERED_EDGES]

    lowered = []

    for edge in edges:
        lowered.append({
            "source": edge.get("from"),
            "target": edge.get("to"),
            "relationship": edge.get("type", "semantic_link"),
        })

    return {
        "lowered_edges": lowered,
        "bounded": True,
        "count": len(lowered),
    }
