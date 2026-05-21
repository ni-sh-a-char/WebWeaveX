from __future__ import annotations

from typing import Any, Dict, List


def balance_semantic_workloads(
    workloads: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:

    ordered_nodes = sorted(workloads.keys())

    total = sum(len(v) for v in workloads.values())

    target = max(1, total // max(1, len(ordered_nodes)))

    balanced = {}

    overflow = []

    for node in ordered_nodes:
        tasks = list(workloads[node])

        while len(tasks) > target:
            overflow.append(tasks.pop())

        balanced[node] = tasks

    for node in ordered_nodes:
        while len(balanced[node]) < target and overflow:
            balanced[node].append(overflow.pop())

    return {
        "balanced": balanced,
        "deterministic": True,
    }
