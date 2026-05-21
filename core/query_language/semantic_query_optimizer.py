from __future__ import annotations

from typing import Any, Dict


def optimize_semantic_query(
    plan: Dict[str, Any],
) -> Dict[str, Any]:

    optimized_steps = sorted(
        plan.get("steps", []),
        key=lambda x: x.get("operation", ""),
    )

    return {
        "steps": optimized_steps,
        "limit": plan.get("limit", 100),
        "optimized": True,
    }
