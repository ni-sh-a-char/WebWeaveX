from __future__ import annotations

from typing import Any, Dict


def build_query_plan(
    query: Dict[str, Any],
) -> Dict[str, Any]:

    query_type = query.get(
        "type",
        "semantic",
    )

    return {
        "query_type": query_type,
        "planner": "v2",
        "deterministic": True,
        "steps": [
            "validate",
            "resolve",
            "execute",
            "reconcile",
        ],
    }
