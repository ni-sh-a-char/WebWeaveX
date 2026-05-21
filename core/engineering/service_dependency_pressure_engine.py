from __future__ import annotations

from typing import Any, Dict, List


def compute_dependency_pressure(
    graph: Dict[str, Any],
) -> Dict[str, Any]:

    edges = list(
        graph.get(
            "edges",
            [],
        )
    )

    pressure: Dict[str, int] = {}

    for edge in edges:

        target = str(
            edge.get("to")
        )

        pressure[target] = (
            pressure.get(
                target,
                0,
            )
            + 1
        )

    return {
        "dependency_pressure": dict(
            sorted(pressure.items())
        ),
    }
