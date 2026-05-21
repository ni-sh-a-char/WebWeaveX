from __future__ import annotations

from typing import Dict, Set, Tuple

from .graph_reconstruction_engine import reconstruct_graph


def reconcile_graphs(*graphs: Dict[str, object]) -> Dict[str, object]:
    merged_nodes = []
    merged_edges = []
    seen_edges: Set[Tuple[str, str]] = set()
    for g in graphs:
        if not isinstance(g, dict):
            continue
        merged_nodes.extend(g.get("nodes", []) or [])
        for e in g.get("edges", []) or []:
            if not isinstance(e, dict):
                continue
            key = (str(e.get("from", "")), str(e.get("to", "")))
            if key in seen_edges:
                continue
            seen_edges.add(key)
            merged_edges.append({"from": key[0], "to": key[1]})
    return reconstruct_graph({"nodes": merged_nodes, "edges": merged_edges})
