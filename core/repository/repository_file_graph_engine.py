from __future__ import annotations

from typing import Any, Dict, List

MAX_EDGES = 100000


def build_repository_file_graph(
    files: List[Dict[str, Any]],
    edges: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    nodes = []

    for file in files:
        path = file["path"]

        nodes.append({
            "id": path,
            "type": "file",
        })

    graph_edges = list(edges or [])[:MAX_EDGES]

    return {
        "nodes": sorted(nodes, key=lambda x: x["id"]),
        "edges": sorted(
            graph_edges,
            key=lambda x: (
                str(x.get("from")),
                str(x.get("to")),
            ),
        ),
        "bounded": True,
    }
