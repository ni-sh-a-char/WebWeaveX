from __future__ import annotations


def merge_graphs(graphs: list):
    nodes = set()
    edges = set()
    max_edges = 0
    for g in graphs or []:
        for n in g.get("nodes", []):
            nid = n.get("id", "") if isinstance(n, dict) else str(n)
            if nid:
                nodes.add(nid)
        for e in g.get("edges", []):
            if isinstance(e, dict) and "from" in e and "to" in e and "type" not in e:
                edges.add((e.get("from", ""), e.get("to", "")))
        max_edges = max(max_edges, int(g.get("max_edges", 0) or 0))
    return {
        "nodes": [{"id": n, "kind": "structural", "metadata": {}} for n in sorted(nodes)],
        "edges": [{"from": a, "to": b} for a, b in sorted(edges)],
        "max_edges": max_edges,
    }
