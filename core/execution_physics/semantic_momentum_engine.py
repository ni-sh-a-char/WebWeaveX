from __future__ import annotations

from typing import Any, Dict


MAX_MOMENTUM = 100000


def compute_semantic_momentum(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = runtime_ir.get(
        "transitions",
        [],
    )

    momentum = min(
        len(transitions),
        MAX_MOMENTUM,
    )

    return {
        "runtime_momentum": momentum,
        "bounded": True,
    }
