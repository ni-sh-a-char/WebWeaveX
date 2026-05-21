from __future__ import annotations

from ._helpers import node_ids


def graph_cluster(graph: dict):
    groups = {}
    for n in node_ids(graph):
        key = n.split("/")[0] if "/" in n else n.split(".")[0]
        groups.setdefault(key, []).append(n)
    return {"clusters": [{"id": k, "nodes": sorted(v)} for k, v in sorted(groups.items())]}
