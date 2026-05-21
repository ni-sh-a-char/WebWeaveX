from __future__ import annotations

from typing import Any, Dict, List


MAX_TASKS = 10000


def build_semantic_task_graph(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    bounded = tasks[:MAX_TASKS]

    edges = []

    for idx in range(len(bounded) - 1):
        edges.append(
            {
                "from": bounded[idx].get("id"),
                "to": bounded[idx + 1].get("id"),
            }
        )

    return {
        "tasks": bounded,
        "edges": edges,
    }
