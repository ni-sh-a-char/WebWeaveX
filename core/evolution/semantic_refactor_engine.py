from __future__ import annotations

from typing import Any, Dict, List


MAX_REFACTORS = 1000


def suggest_semantic_refactors(
    repository_ir: Dict[str, Any],
) -> Dict[str, Any]:

    nodes = list(
        repository_ir.get(
            "nodes",
            [],
        )
    )

    suggestions = []

    for idx, node in enumerate(
        nodes[:MAX_REFACTORS]
    ):

        suggestions.append(
            {
                "node": node.get("id"),
                "suggestion": "review_structure",
            }
        )

    return {
        "suggestions": suggestions,
        "bounded": True,
    }
