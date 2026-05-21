from __future__ import annotations

from typing import Any, Dict, List


MAX_NODES = 128


def schedule_distributed_execution(
    tasks: List[Dict[str, Any]],
    nodes: List[str],
) -> Dict[str, Any]:

    if not nodes:
        nodes = ["node_a"]

    bounded_nodes = sorted(nodes)[:MAX_NODES]

    scheduled = []

    for idx, task in enumerate(tasks):
        node = bounded_nodes[idx % len(bounded_nodes)]

        scheduled.append({
            "task": task,
            "node": node,
        })

    return {
        "scheduled": scheduled,
        "deterministic": True,
    }
