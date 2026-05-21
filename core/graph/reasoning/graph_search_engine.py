from __future__ import annotations

from ._helpers import node_ids


def graph_search(graph: dict, query: str):
    q = (query or "").lower()
    nodes = [n for n in node_ids(graph) if q in n.lower()]
    edges = [
        e
        for e in (graph or {}).get("edges", [])
        if isinstance(e, dict) and q in f"{e.get('from', '')}{e.get('to', '')}".lower()
    ]
    return {
        "nodes": sorted(set(nodes)),
        "edges": sorted(edges, key=lambda e: (e.get("from", ""), e.get("to", ""))),
    }
