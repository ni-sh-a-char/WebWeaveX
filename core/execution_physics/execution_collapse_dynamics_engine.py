from __future__ import annotations

from typing import Any, Dict


COLLAPSE_THRESHOLD = 10000


def analyze_collapse_dynamics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    pressure = int(
        runtime_ir.get("execution_physics", {}).get(
            "execution_pressure", 0
        )
        if isinstance(runtime_ir.get("execution_physics"), dict)
        else 0
    )
    collapse_risk = (
        "imminent"
        if pressure > COLLAPSE_THRESHOLD
        else "contained"
    )
    return {
        "collapse_risk": collapse_risk,
        "pressure": pressure,
    }
