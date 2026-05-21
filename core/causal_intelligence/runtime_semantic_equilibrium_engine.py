from __future__ import annotations

from typing import Any, Dict


def assess_semantic_equilibrium(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    equilibrium = runtime_ir.get("runtime_equilibrium", {})
    if not isinstance(equilibrium, dict):
        entropy = runtime_ir.get("runtime_entropy", {})
        score = int(entropy.get("entropy_score", 0))
        state = "stable" if score < 100 else "unstable"
    else:
        state = equilibrium.get("equilibrium", "unknown")
    pressure = runtime_ir.get("execution_pressure", {})
    pressure_score = int(pressure.get("pressure_score", 0))
    balanced = state == "stable" and pressure_score < 5000
    return {
        "semantic_equilibrium": state,
        "balanced": balanced,
    }
