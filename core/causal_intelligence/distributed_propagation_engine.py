from __future__ import annotations

from typing import Any, Dict, List


MAX_PROPAGATION = 10000


def propagate_distributed_state(
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

    propagation = []

    for edge in edges:

        propagation.append(
            {
                "source": edge.get("from"),
                "target": edge.get("to"),
                "propagates": True,
            }
        )

    return {
        "propagation_paths": sorted(
            propagation,
            key=lambda x: (
                str(x["source"]),
                str(x["target"]),
            ),
        )[:MAX_PROPAGATION],
        "bounded": True,
    }
