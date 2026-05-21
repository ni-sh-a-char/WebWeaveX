from __future__ import annotations

from collections import deque
from typing import Any, Dict, List


MAX_VISITS = 100000


def traverse_repository_world(
    graph: Dict[str, Any],
    start: str,
) -> Dict[str, Any]:

    queue = deque([start])

    visited: List[str] = []
    seen = set()

    while queue and len(visited) < MAX_VISITS:

        node = queue.popleft()

        if node in seen:
            continue

        seen.add(node)
        visited.append(node)

        neighbors = sorted(
            str(edge.get("to"))
            for edge in graph.get("edges", [])
            if edge.get("from") == node and edge.get("to")
        )

        for nxt in neighbors:
            if nxt not in seen:
                queue.append(nxt)

    return {
        "visited": visited,
        "count": len(visited),
        "bounded": len(visited) < MAX_VISITS,
    }
