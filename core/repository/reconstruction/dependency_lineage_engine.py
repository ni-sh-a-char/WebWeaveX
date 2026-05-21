from __future__ import annotations

def build_dependency_lineage(deps: list[str]):
    d = sorted(set(deps or []))
    edges = [{"from": d[i], "to": d[i+1]} for i in range(max(0, len(d)-1))]
    return {"nodes": d, "edges": edges}
