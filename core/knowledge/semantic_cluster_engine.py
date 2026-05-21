from __future__ import annotations


def cluster_semantic_graph(graph: dict):
    nodes = sorted(set((graph or {}).get("nodes", [])))
    clusters = {}
    for n in nodes:
        key = n.split(".")[0] if "." in n else n[:1].lower()
        clusters.setdefault(key, []).append(n)
    return {"clusters": {k: sorted(v) for k, v in sorted(clusters.items())}}
