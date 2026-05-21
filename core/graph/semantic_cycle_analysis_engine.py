from __future__ import annotations

from typing import Any, Dict, List, Set


def detect_cycles(graph: Dict[str, Any], max_depth: int = 50) -> Dict[str, Any]:
    edges = graph.get("edges", []) or []
    adj: Dict[str, List[str]] = {}
    for e in edges:
        if isinstance(e, dict) and e.get("from") and e.get("to"):
            adj.setdefault(str(e["from"]), []).append(str(e["to"]))
    cycles: List[List[str]] = []
    visited: Set[str] = set()
    stack: Set[str] = set()
    path: List[str] = []

    def dfs(n: str, depth: int) -> None:
        if depth > max_depth:
            return
        if n in stack:
            if n in path:
                i = path.index(n)
                cycles.append(path[i:] + [n])
            return
        if n in visited:
            return
        visited.add(n)
        stack.add(n)
        path.append(n)
        for nb in adj.get(n, []):
            dfs(nb, depth + 1)
        path.pop()
        stack.remove(n)

    for start in list(adj.keys())[:100]:
        dfs(start, 0)
    return {
        "cycles": cycles[:20],
        "cycle_count": len(cycles),
        "bounded": max_depth,
        "contradiction_pressure": min(1.0, len(cycles) * 0.2),
    }
