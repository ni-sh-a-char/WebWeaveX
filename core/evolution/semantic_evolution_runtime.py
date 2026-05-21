from __future__ import annotations

from typing import Any, Dict


MAX_EVOLUTION_DEPTH = 1000


def evolve_semantic_runtime(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    keys = sorted(runtime.keys())

    evolution_steps = []

    for idx, key in enumerate(
        keys[:MAX_EVOLUTION_DEPTH]
    ):

        evolution_steps.append(
            {
                "step": idx,
                "key": key,
                "action": "preserve",
            }
        )

    return {
        "evolution_steps": evolution_steps,
        "evolution_size": len(
            evolution_steps
        ),
        "bounded": True,
    }
