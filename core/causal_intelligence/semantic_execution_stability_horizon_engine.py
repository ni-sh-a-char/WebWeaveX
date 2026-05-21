from __future__ import annotations

from typing import Any, Dict


def forecast_stability_horizon(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    instability = runtime_ir.get("instability_forecast", {})
    if isinstance(instability, dict):
        level = instability.get("instability_forecast", "low")
    else:
        level = "low"
    horizon = (
        "short"
        if level == "high"
        else "long"
    )
    return {
        "stability_horizon": horizon,
        "instability_level": level,
    }
