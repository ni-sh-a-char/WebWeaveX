from __future__ import annotations

def graph_lineage(graph: dict):
    return {"node_count": len(graph.get('nodes',[])), "edge_count": len(graph.get('edges',[]))}
