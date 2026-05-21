from __future__ import annotations

from typing import Dict, List


def query_nodes(graph: Dict[str, object], node: str = "") -> List[dict]:
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    if not node:
        return [n for n in nodes if isinstance(n, dict)]
    return [n for n in nodes if isinstance(n, dict) and n.get("id") == node]


def query_edges(graph: Dict[str, object], node: str = "") -> List[dict]:
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    if not node:
        return [e for e in edges if isinstance(e, dict)]
    return [
        e
        for e in edges
        if isinstance(e, dict) and (e.get("from") == node or e.get("to") == node)
    ]
