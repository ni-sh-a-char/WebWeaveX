from __future__ import annotations

from typing import Any, Dict


def compute_architectural_pressure(
    graph: Dict[str, Any],
) -> Dict[str, Any]:
    node_count = len(graph.get("nodes", []))
    edge_count = len(graph.get("edges", []))
    pressure = round(
        edge_count / max(node_count, 1),
        3,
    )
    return {
        "architectural_pressure": pressure,
        "node_count": node_count,
        "edge_count": edge_count,
    }
