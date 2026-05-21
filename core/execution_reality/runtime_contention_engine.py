from __future__ import annotations

from typing import Any, Dict


MAX_HOTSPOTS = 1000


def analyze_runtime_contention(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    edges = list(
        topology.get(
            "edges",
            [],
        )
    )

    contention: Dict[str, int] = {}

    for edge in edges:

        target = str(
            edge.get("to")
        )

        contention[target] = (
            contention.get(
                target,
                0,
            )
            + 1
        )

    return {
        "contention": dict(
            sorted(contention.items())
        ),
        "hotspots": sorted(
            contention.keys()
        )[:MAX_HOTSPOTS],
    }
