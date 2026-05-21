from __future__ import annotations

from typing import Any, Dict, List


def partition_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    parent: Dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for n in nodes:
        if isinstance(n, dict) and n.get("id"):
            find(str(n["id"]))
    for e in edges:
        if isinstance(e, dict) and e.get("from") and e.get("to"):
            union(str(e["from"]), str(e["to"]))
    components: Dict[str, List[str]] = {}
    for x in parent:
        root = find(x)
        components.setdefault(root, []).append(x)
    return {"partitions": list(components.values()), "count": len(components)}
