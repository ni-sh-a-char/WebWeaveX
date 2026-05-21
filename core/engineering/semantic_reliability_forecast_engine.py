from __future__ import annotations

from typing import Any, Dict


MAX_STABLE_TRANSITIONS = 1000


def forecast_semantic_reliability(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = runtime_ir.get(
        "transitions",
        [],
    )

    reliability = (
        "stable"
        if len(transitions) < MAX_STABLE_TRANSITIONS
        else "degraded"
    )

    return {
        "reliability": reliability,
    }
