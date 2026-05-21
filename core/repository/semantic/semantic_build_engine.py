from __future__ import annotations

from typing import Dict, List


def infer_semantic_build_graph(package_managers: List[str]) -> Dict[str, List[dict]]:
    nodes = sorted(set(package_managers or []))
    edges = []
    for i in range(len(nodes) - 1):
        edges.append({"from": nodes[i], "to": nodes[i + 1]})
    return {"nodes": nodes, "edges": edges}
