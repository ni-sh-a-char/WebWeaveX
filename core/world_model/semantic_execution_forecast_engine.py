from __future__ import annotations

from typing import Any, Dict, List


MAX_FORECAST_NODES = 10000


def forecast_semantic_execution(
    topology: Dict[str, Any],
) -> Dict[str, Any]:

    nodes = topology.get(
        "nodes",
        [],
    )[:MAX_FORECAST_NODES]

    execution_order = sorted(
        str(node.get("id"))
        for node in nodes
        if node.get("id")
    )

    return {
        "forecast_order": execution_order,
        "forecast_size": len(
            execution_order
        ),
        "bounded": True,
    }
