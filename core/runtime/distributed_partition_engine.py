from __future__ import annotations

from typing import Any, Dict, List


def partition_runtime_graph(
    nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:

    partitions = {}

    for node in nodes:

        region = node.get(
            "region",
            "default",
        )

        partitions.setdefault(
            region,
            [],
        ).append(node)

    return {
        "partitions": partitions,
        "count": len(partitions),
    }
