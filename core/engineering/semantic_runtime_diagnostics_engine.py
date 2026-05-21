from __future__ import annotations

from typing import Any, Dict


MAX_HEALTHY_GRAPH = 100000


def diagnose_semantic_runtime(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    graph_db = runtime_ir.get(
        "graph_database",
        {},
    )
    graph_size = (
        len(graph_db)
        if isinstance(graph_db, dict)
        else 0
    )

    healthy = graph_size < MAX_HEALTHY_GRAPH

    return {
        "healthy": healthy,
        "graph_size": graph_size,
    }
