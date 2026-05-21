from __future__ import annotations


def build_framework_relationships(frameworks: list, services: list):
    fw = sorted(set(frameworks or []))
    svc = sorted(set(services or []))
    edges = []
    for s in svc:
        for f in fw[:3]:
            edges.append({"from": s, "to": f})
    return {"nodes": sorted(set(fw + svc)), "edges": sorted(edges, key=lambda x: (x["from"], x["to"]))}
