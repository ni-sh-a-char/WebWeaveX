from __future__ import annotations

from typing import Any, Dict


def forecast_runtime_load(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    pressure = runtime_ir.get("execution_pressure", {})
    score = int(pressure.get("pressure_score", 0))
    load_tier = (
        "high"
        if score > 1000
        else "normal"
        if score > 0
        else "idle"
    )
    return {
        "load_tier": load_tier,
        "projected_load": score,
    }
