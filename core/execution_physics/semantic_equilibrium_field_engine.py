from __future__ import annotations

from typing import Any, Dict


def build_equilibrium_field(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    physics = runtime_ir.get("execution_physics", {})
    pressure = int(
        physics.get("execution_pressure", 0)
        if isinstance(physics, dict)
        else 0
    )
    field_state = (
        "equilibrium"
        if pressure < 1000
        else "disequilibrium"
    )
    return {
        "field_state": field_state,
        "field_pressure": pressure,
    }
