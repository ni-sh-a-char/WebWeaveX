from __future__ import annotations

from typing import Any, Dict


COLLAPSE_THRESHOLD = 10000


def forecast_execution_collapse(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    pressure = runtime_ir.get(
        "execution_pressure",
        {},
    )

    score = int(
        pressure.get(
            "pressure_score",
            0,
        )
    )

    collapse_risk = (
        "high"
        if score > COLLAPSE_THRESHOLD
        else "low"
    )

    return {
        "collapse_risk": collapse_risk,
    }
