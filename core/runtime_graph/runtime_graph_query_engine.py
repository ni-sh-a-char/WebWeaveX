from __future__ import annotations

from typing import Any, Dict, List

MAX_RESULTS = 1000


def query_runtime_graph(
    graph: Dict[str, Any],
    query: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = list(graph.get("nodes", []) or [])

    node_type = str(
        query.get("type", "")
    ).strip()

    results: List[Dict[str, Any]] = []

    for node in nodes:
        if node_type:
            if str(node.get("type", "")) != node_type:
                continue

        results.append(node)

        if len(results) >= MAX_RESULTS:
            break

    return {
        "results": results,
        "count": len(results),
        "bounded": True,
    }
