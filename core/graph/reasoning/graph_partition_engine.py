from __future__ import annotations

from ._helpers import node_ids


def graph_partition(graph: dict, partitions: int = 4):
    p = max(1, int(partitions))
    nodes = node_ids(graph)
    out = {str(i): [] for i in range(p)}
    for i, n in enumerate(nodes):
        out[str(i % p)].append(n)
    return out
