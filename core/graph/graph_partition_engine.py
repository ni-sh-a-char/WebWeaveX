from __future__ import annotations

from typing import Dict, List


def partition_graph(graph: Dict[str, object], parts: int = 2) -> Dict[str, object]:
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    buckets: List[List[dict]] = [[] for _ in range(max(1, parts))]
    for i, node in enumerate(nodes):
        if isinstance(node, dict):
            buckets[i % len(buckets)].append(node)
    return {"partitions": buckets, "partition_count": len(buckets)}
