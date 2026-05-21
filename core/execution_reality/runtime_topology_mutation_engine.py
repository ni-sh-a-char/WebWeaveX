from __future__ import annotations

from typing import Any, Dict


def mutate_runtime_topology(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    node_count = len(
        topology.get(
            "nodes",
            [],
        )
    )

    return {
        "topology_mutation": {
            "predicted_growth": (
                node_count + 1
            ),
        },
    }
