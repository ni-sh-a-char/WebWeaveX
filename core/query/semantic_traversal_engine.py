from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Set

MAX_TRAVERSAL_DEPTH = 50


def traverse_graph(
    adjacency: Dict[str, List[str]],
    start: str,
) -> List[str]:
    visited: Set[str] = set()
    queue = deque([(start, 0)])
    ordered: List[str] = []
    while queue:
        node, depth = queue.popleft()
        if depth > MAX_TRAVERSAL_DEPTH:
            continue
        if node in visited:
            continue
        visited.add(node)
        ordered.append(node)
        for nxt in sorted(adjacency.get(node, [])):
            queue.append((nxt, depth + 1))
    return ordered


def semantic_traverse(graph: Dict[str, Any], start: str, max_depth: int = 10) -> Dict[str, Any]:
    edges = graph.get("edges", []) or []
    adj: Dict[str, List[str]] = {}
    for e in edges:
        if isinstance(e, dict) and e.get("from") and e.get("to"):
            adj.setdefault(str(e["from"]), []).append(str(e["to"]))
    visited: Set[str] = set()
    order: List[str] = []

    def dfs(n: str, d: int) -> None:
        if d > max_depth or n in visited:
            return
        visited.add(n)
        order.append(n)
        for nb in adj.get(n, []):
            dfs(nb, d + 1)

    if start:
        dfs(start, 0)
    return {"order": order, "visited_count": len(visited), "max_depth": max_depth, "bounded": True}
