from __future__ import annotations

from typing import Any, Dict


def assess_stability_mechanics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    physics = runtime_ir.get("execution_physics", {})
    state = (
        physics.get("physics_state", "unknown")
        if isinstance(physics, dict)
        else "unknown"
    )
    coherence = runtime_ir.get("execution_coherence", {})
    coherent = (
        coherence.get("coherent", False)
        if isinstance(coherence, dict)
        else False
    )
    stable = state == "stable" and coherent
    return {
        "stable": stable,
        "physics_state": state,
    }
