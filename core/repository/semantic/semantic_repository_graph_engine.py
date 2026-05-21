from __future__ import annotations

from typing import Dict, List


def build_semantic_repository_graph(parts: Dict[str, object]) -> Dict[str, List[dict]]:
    p = parts or {}
    nodes = set()
    for key in ["symbols", "frameworks", "dependencies", "services", "routes"]:
        values = p.get(key, [])
        if isinstance(values, dict):
            values = list(values.values())
        if isinstance(values, list):
            for v in values:
                if isinstance(v, str):
                    nodes.add(v)

    ordered_nodes = sorted(nodes)
    edges = [{"from": ordered_nodes[i], "to": ordered_nodes[i + 1]} for i in range(max(0, len(ordered_nodes) - 1))]
    return {"nodes": ordered_nodes, "edges": edges}
