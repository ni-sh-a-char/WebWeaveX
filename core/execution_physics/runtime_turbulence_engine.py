from __future__ import annotations

from typing import Any, Dict


TURBULENCE_THRESHOLD = 1000


def analyze_runtime_turbulence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    entropy = runtime_ir.get(
        "runtime_entropy",
        {},
    )

    entropy_score = int(
        entropy.get(
            "entropy_score",
            0,
        )
        if isinstance(entropy, dict)
        else 0
    )

    turbulence = (
        "high"
        if entropy_score > TURBULENCE_THRESHOLD
        else "low"
    )

    return {
        "runtime_turbulence": turbulence,
        "entropy_score": entropy_score,
    }
