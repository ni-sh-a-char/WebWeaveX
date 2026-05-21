from __future__ import annotations

from typing import Any, Dict


MAX_BOTTLENECKS = 1000
BOTTLENECK_THRESHOLD = 3


def detect_execution_bottlenecks(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    edges = topology.get(
        "edges",
        [],
    )

    inbound: Dict[str, int] = {}

    for edge in edges:

        target = str(
            edge.get("to")
        )

        inbound[target] = (
            inbound.get(
                target,
                0,
            )
            + 1
        )

    bottlenecks = []

    for node, degree in inbound.items():

        if degree >= BOTTLENECK_THRESHOLD:

            bottlenecks.append(
                {
                    "node": node,
                    "pressure": degree,
                }
            )

    return {
        "bottlenecks": sorted(
            bottlenecks,
            key=lambda x: (
                -x["pressure"],
                x["node"],
            ),
        )[:MAX_BOTTLENECKS],
    }
