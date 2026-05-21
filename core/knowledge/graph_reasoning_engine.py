from __future__ import annotations


def reason_over_semantic_graph(graph: dict):
    nodes = (graph or {}).get("nodes", [])
    edges = (graph or {}).get("edges", [])
    adjacency = {}
    for e in edges:
        adjacency.setdefault(e.get("from"), 0)
        adjacency[e.get("from")] += 1
    hubs = sorted(adjacency.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "connected": len(edges) > 0,
        "hubs": [{"node": n, "out_degree": d} for n, d in hubs],
    }
