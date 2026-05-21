from __future__ import annotations

def enforce_graph_budget(nodes: int, edges: int, max_nodes: int = 5000, max_edges: int = 20000):
    return {"nodes_ok": nodes <= max_nodes, "edges_ok": edges <= max_edges}
