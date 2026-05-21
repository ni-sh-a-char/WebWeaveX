from __future__ import annotations

from typing import Any, Dict, List


MAX_RESULTS = 1000


def execute_semantic_query(
    nodes: List[Dict[str, Any]],
    filters: Dict[str, Any],
) -> Dict[str, Any]:

    results = []

    for node in nodes:
        match = True

        for key, value in filters.items():
            if node.get(key) != value:
                match = False
                break

        if match:
            results.append(node)

        if len(results) >= MAX_RESULTS:
            break

    return {
        "results": results,
        "count": len(results),
    }
