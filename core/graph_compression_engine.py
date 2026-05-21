from __future__ import annotations

def compress_graph(graph: dict, max_edges: int = 20000):
    return {"nodes": graph.get('nodes',[]), "edges": graph.get('edges',[])[:max_edges], "max_edges": max_edges}
