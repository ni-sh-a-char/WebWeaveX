from __future__ import annotations

from typing import Any, Dict, List


MAX_RESULTS = 1000


def execute_semantic_plan(
    plan: Dict[str, Any],
    dataset: List[Dict[str, Any]],
) -> Dict[str, Any]:

    results = []

    filters = {}

    for step in plan.get("steps", []):
        if step.get("operation") == "scan":
            filters = step.get("filters", {})

    limit = min(plan.get("limit", MAX_RESULTS), MAX_RESULTS)

    for item in dataset:
        matched = True

        for key, value in filters.items():
            if str(item.get(key)) != str(value):
                matched = False
                break

        if matched:
            results.append(item)

        if len(results) >= limit:
            break

    return {
        "results": results,
        "count": len(results),
    }
