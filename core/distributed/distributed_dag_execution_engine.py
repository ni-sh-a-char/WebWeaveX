from __future__ import annotations

from typing import Any, Dict, List


MAX_DAG_NODES = 10000


def execute_semantic_dag(
    nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        nodes,
        key=lambda x: str(x.get("id")),
    )[:MAX_DAG_NODES]

    execution_order = []

    for node in ordered:
        execution_order.append(node.get("id"))

    return {
        "execution_order": execution_order,
        "deterministic": True,
    }
