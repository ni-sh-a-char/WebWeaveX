"""Runtime graph builder for cross-language parity — matches javascript/src/graph/runtimeGraph.ts."""
from __future__ import annotations

from typing import Any


def normalize_runtime_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(
        list(graph.get("nodes") or []),
        key=lambda n: f"{n.get('id', '')}|{n.get('type', '')}|{n.get('name', '')}",
    )
    edges = sorted(
        list(graph.get("edges") or []),
        key=lambda e: (
            f"{e.get('source') or e.get('from', '')}|"
            f"{e.get('target') or e.get('to', '')}|{e.get('type', '')}"
        ),
    )
    return {"nodes": nodes, "edges": edges, "bounded": True}


def build_parity_runtime_graph(sources: dict[str, Any]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    idx = 0
    for kind, payload in sorted(sources.items(), key=lambda kv: kv[0]):
        nodes.append({"id": f"node:{kind}:{idx}", "type": kind, "payload": payload})
        idx += 1
    if len(nodes) > 1:
        for i in range(1, len(nodes)):
            edges.append(
                {
                    "source": nodes[0]["id"],
                    "target": nodes[i]["id"],
                    "type": "runtime_link",
                }
            )
    return normalize_runtime_graph({"nodes": nodes, "edges": edges, "bounded": True})
