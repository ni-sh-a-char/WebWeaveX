from __future__ import annotations

from typing import Any, Dict, List


MAX_RESULTS = 1000


def semantic_repository_search(
    query: str,
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    results = []

    lowered = query.lower()

    for ir in repository_irs:

        path = str(
            ir.get("path", "")
        ).lower()

        if lowered in path:

            results.append(
                {
                    "path": ir.get("path"),
                }
            )

    return {
        "results": results[
            :MAX_RESULTS
        ],
        "count": len(results[:MAX_RESULTS]),
    }
