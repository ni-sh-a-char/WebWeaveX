from __future__ import annotations

from typing import Any, Dict, List


MAX_PROPAGATION = 10000


def propagate_runtime_energy(
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

    propagation: List[Dict[str, Any]] = []

    for edge in edges[:MAX_PROPAGATION]:

        propagation.append(
            {
                "from": edge.get("from"),
                "to": edge.get("to"),
                "energy_transfer": 1,
            }
        )

    return {
        "energy_propagation": sorted(
            propagation,
            key=lambda x: (
                str(x["from"]),
                str(x["to"]),
            ),
        ),
        "bounded": True,
    }
