from __future__ import annotations

from typing import Any, Dict, List


def optimize_semantic_architecture(
    graph: Dict[str, Any],
) -> Dict[str, Any]:

    nodes = sorted(
        graph.get("nodes", []),
        key=lambda x: str(
            x.get("id")
        ),
    )

    return {
        "optimized_nodes": nodes,
        "optimization_count": len(
            nodes
        ),
    }
