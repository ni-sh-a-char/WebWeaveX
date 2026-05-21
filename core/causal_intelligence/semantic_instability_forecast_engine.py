from __future__ import annotations

from typing import Any, Dict


INSTABILITY_PRESSURE_THRESHOLD = 5000


def forecast_runtime_instability(
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

    instability = (
        "high"
        if score > INSTABILITY_PRESSURE_THRESHOLD
        else "low"
    )

    return {
        "instability_forecast": instability,
        "pressure_score": score,
    }
