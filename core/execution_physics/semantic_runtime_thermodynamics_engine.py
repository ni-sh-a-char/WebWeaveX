from __future__ import annotations

from typing import Any, Dict


def analyze_runtime_thermodynamics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    pressure = int(
        runtime_ir.get("execution_physics", {}).get(
            "execution_pressure", 0
        )
        if isinstance(runtime_ir.get("execution_physics"), dict)
        else 0
    )
    entropy = int(
        runtime_ir.get("runtime_entropy", {}).get(
            "entropy_score", 0
        )
        if isinstance(runtime_ir.get("runtime_entropy"), dict)
        else 0
    )
    temperature = min(pressure + entropy, 100000)
    return {
        "temperature": temperature,
        "thermodynamic_state": (
            "hot" if temperature > 1000 else "cool"
        ),
    }
