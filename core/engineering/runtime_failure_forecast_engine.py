from __future__ import annotations

from typing import Any, Dict, List


MAX_FAILURES = 1000


def forecast_runtime_failures(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = list(
        runtime_ir.get(
            "transitions",
            [],
        )
    )

    forecasts = []

    for idx, transition in enumerate(
        transitions[:MAX_FAILURES]
    ):

        forecasts.append(
            {
                "transition": transition,
                "risk": "low",
            }
        )

    return {
        "forecast_count": len(
            forecasts
        ),
        "forecasts": forecasts,
        "bounded": True,
    }
