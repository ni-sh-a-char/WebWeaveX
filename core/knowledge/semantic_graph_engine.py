from __future__ import annotations


def build_semantic_graph(parts: dict):
    nodes = sorted(set(parts.get("nodes", [])))
    edges = sorted(
        {(
            e.get("from", ""),
            e.get("to", ""),
        ) for e in parts.get("edges", []) if isinstance(e, dict) and e.get("from") and e.get("to")}
    )
    return {"nodes": nodes, "edges": [{"from": f, "to": t} for f, t in edges]}
