from __future__ import annotations

from typing import Any, Dict


def trigger_semantic_reflex(
    runtime_state: Dict[str, Any],
) -> Dict[str, Any]:

    overloaded = (
        runtime_state.get(
            "cpu_units",
            0,
        ) > 100
    )

    return {
        "reflex_triggered": overloaded,
    }
