from __future__ import annotations

def build_distributed_graph(services: list[str], dependencies: list[str]):
    svc = sorted(set(services or []))
    dep = sorted(set(dependencies or []))
    edges = []
    for s in svc:
        for d in dep[:5]:
            edges.append({"from": s, "to": d})
    return {"nodes": sorted(set(svc + dep)), "edges": sorted(edges, key=lambda x: (x["from"], x["to"]))}
