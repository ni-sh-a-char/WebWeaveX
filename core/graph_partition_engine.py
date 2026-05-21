from __future__ import annotations

def partition_graph(graph: dict, parts: int = 2):
    nodes=graph.get('nodes',[])
    buckets=[[] for _ in range(max(1,parts))]
    for i,n in enumerate(nodes): buckets[i%len(buckets)].append(n)
    return {"partitions": buckets}
