from __future__ import annotations

from collections import deque

from typing import Any, Dict, List


MAX_GRAPH_VISITS = 10000


def traverse_large_graph(
    graph: Dict[str, Any],
    start: str,
) -> Dict[str, Any]:

    adjacency = {}

    for edge in graph.get("edges", []):

        adjacency.setdefault(
            edge["from"],
            [],
        ).append(edge["to"])

    queue = deque([start])

    visited = []

    seen = set()

    while queue and len(visited) < MAX_GRAPH_VISITS:

        node = queue.popleft()

        if node in seen:
            continue

        seen.add(node)

        visited.append(node)

        for nxt in sorted(adjacency.get(node, [])):
            queue.append(nxt)

    return {
        "visited": visited,
        "count": len(visited),
        "bounded": True,
    }
