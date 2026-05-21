from __future__ import annotations

from typing import Any, Dict


def measure_runtime_resonance(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    pressure = int(
        runtime_ir.get("execution_pressure", {}).get(
            "pressure_score", 0
        )
    )
    entropy = int(
        runtime_ir.get("runtime_entropy", {}).get(
            "entropy_score", 0
        )
    )
    resonance = min(pressure + entropy, 100000)
    return {
        "resonance_score": resonance,
        "amplified": resonance > 1000,
    }
