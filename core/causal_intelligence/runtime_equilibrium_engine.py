from __future__ import annotations

from typing import Any, Dict


EQUILIBRIUM_ENTROPY_THRESHOLD = 100


def compute_runtime_equilibrium(
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
    )

    equilibrium = (
        "stable"
        if entropy_score < EQUILIBRIUM_ENTROPY_THRESHOLD
        else "unstable"
    )

    return {
        "equilibrium": equilibrium,
        "entropy_score": entropy_score,
    }
