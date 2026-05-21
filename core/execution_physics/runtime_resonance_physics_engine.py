from __future__ import annotations

from typing import Any, Dict


MAX_RESONANCE = 100000


def compute_resonance_physics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    momentum = int(
        runtime_ir.get("semantic_momentum", {}).get(
            "runtime_momentum", 0
        )
        if isinstance(runtime_ir.get("semantic_momentum"), dict)
        else 0
    )
    entropy = int(
        runtime_ir.get("runtime_entropy", {}).get(
            "entropy_score", 0
        )
        if isinstance(runtime_ir.get("runtime_entropy"), dict)
        else 0
    )
    resonance = min(momentum + entropy, MAX_RESONANCE)
    return {
        "resonance_amplitude": resonance,
        "amplified": resonance > 500,
    }
