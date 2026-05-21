from __future__ import annotations

from typing import Any, Dict


def measure_execution_coherence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    convergence = runtime_ir.get("state_convergence", {})
    if isinstance(convergence, dict):
        if "converged" in convergence:
            converged = convergence.get("converged", True)
        else:
            converged = (
                convergence.get("equilibrium") == "stable"
            )
    else:
        converged = True
    turbulence = runtime_ir.get("runtime_turbulence", {})
    turb_level = (
        turbulence.get("runtime_turbulence", "low")
        if isinstance(turbulence, dict)
        else "low"
    )
    coherent = converged and turb_level == "low"
    return {
        "coherent": coherent,
        "converged": converged,
    }
