from __future__ import annotations


def build_execution_flow(calls: list):
    pairs = sorted(set((c.get("from", ""), c.get("to", "")) for c in calls or [] if isinstance(c, dict)))
    edges = [{"from": f, "to": t} for f, t in pairs if f and t]
    nodes = sorted(set([x for e in edges for x in (e["from"], e["to"])]))
    return {"nodes": nodes, "edges": edges}
