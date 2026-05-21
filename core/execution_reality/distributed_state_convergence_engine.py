from __future__ import annotations

from typing import Any, Dict


def compute_state_convergence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    crdt = runtime_ir.get(
        "semantic_crdt",
        {},
    )

    conflicts = list(
        crdt.get(
            "conflicts",
            [],
        )
        if isinstance(crdt, dict)
        else []
    )

    converged = len(conflicts) == 0

    return {
        "converged": converged,
        "conflict_count": len(
            conflicts
        ),
    }
