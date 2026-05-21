from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple


MAX_OPT_PASSES = 10


def optimize_semantic_pipeline(ir: Dict[str, Any]) -> Dict[str, Any]:
    edges = list(ir.get("lowered_edges", []))

    optimized: List[Dict[str, Any]] = []

    seen: Set[Tuple[str, str, str]] = set()

    for edge in edges:
        key = (
            str(edge.get("source")),
            str(edge.get("target")),
            str(edge.get("relationship")),
        )

        if key in seen:
            continue

        seen.add(key)

        optimized.append(edge)

    return {
        "optimized_edges": optimized,
        "optimization_passes": 1,
        "deterministic": True,
    }
