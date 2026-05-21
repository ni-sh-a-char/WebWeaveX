from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def route_semantic_tasks(
    tasks: List[
        Dict[str, Any]
    ],
    nodes: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    routed = []

    if not nodes:

        return {
            "routes": [],
        }

    index = 0

    for task in tasks:

        routed.append({
            "task": task,
            "node": nodes[index],
        })

        index = (
            index + 1
        ) % len(nodes)

    return {
        "routes": routed,
    }
