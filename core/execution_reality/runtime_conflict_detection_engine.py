from __future__ import annotations

from typing import Any, Dict, List, Tuple


MAX_CONFLICTS = 1000


def detect_runtime_conflicts(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = runtime_ir.get(
        "transitions",
        [],
    )

    seen = set()

    conflicts: List[Tuple[Any, Any]] = []

    for transition in transitions:

        key = (
            transition.get("from"),
            transition.get("to"),
        )

        if key in seen:

            conflicts.append(key)

        seen.add(key)

    return {
        "conflicts": sorted(
            conflicts,
            key=lambda x: (str(x[0]), str(x[1])),
        )[:MAX_CONFLICTS],
    }
