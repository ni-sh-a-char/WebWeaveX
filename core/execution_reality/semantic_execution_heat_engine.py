from __future__ import annotations

from typing import Any, Dict


MAX_HEATMAP = 1000


def compute_execution_heat(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    nodes = topology.get(
        "nodes",
        [],
    )

    heat = []

    for idx, node in enumerate(
        sorted(
            nodes,
            key=lambda x: str(
                x.get("id")
            ),
        )
    ):

        heat.append(
            {
                "node": node.get("id"),
                "heat": idx + 1,
            }
        )

    return {
        "heatmap": heat[:MAX_HEATMAP],
    }
