from __future__ import annotations

from typing import Any, Dict, Optional


def build_kernel_topology(
    graph: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    graph = graph or {}
    nodes = sorted(graph.get("nodes", []), key=lambda item: str(item.get("id", "")))
    edges = sorted(
        graph.get("edges", []),
        key=lambda item: (
            str(item.get("from", "")),
            str(item.get("to", "")),
            str(item.get("relation", "")),
        ),
    )
    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "bounded": True,
    }
