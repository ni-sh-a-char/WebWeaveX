from __future__ import annotations

def synthesize_knowledge(parts: dict):
    nodes = sorted((parts or {}).keys())
    edges = [{"from": nodes[i], "to": nodes[i+1]} for i in range(max(0, len(nodes)-1))]
    return {"nodes": nodes, "edges": edges}
