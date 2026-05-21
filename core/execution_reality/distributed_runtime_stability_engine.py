from __future__ import annotations

from typing import Any, Dict


MAX_STABLE_PRESSURE = 50000


def assess_distributed_stability(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    pressure = runtime_ir.get("execution_pressure", {})
    score = int(pressure.get("pressure_score", 0))
    return {
        "stable": score < MAX_STABLE_PRESSURE,
        "pressure_score": score,
    }
