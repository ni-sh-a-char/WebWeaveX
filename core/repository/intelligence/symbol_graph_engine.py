from __future__ import annotations

def build_symbol_graph(ast_data: dict):
    nodes = sorted(set(ast_data.get("symbols", [])))
    edges = [{"from": nodes[i], "to": nodes[i+1]} for i in range(max(0, len(nodes)-1))]
    return {"nodes": nodes, "edges": edges}
