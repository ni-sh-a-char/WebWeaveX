from __future__ import annotations

from typing import Any, Dict


def compute_runtime_entropy(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = runtime_ir.get(
        "transitions",
        [],
    )

    unique_states = set()

    for transition in transitions:

        unique_states.add(
            str(
                transition.get("from")
            )
        )

        unique_states.add(
            str(
                transition.get("to")
            )
        )

    entropy_score = len(
        unique_states
    )

    return {
        "entropy_score": entropy_score,
    }
