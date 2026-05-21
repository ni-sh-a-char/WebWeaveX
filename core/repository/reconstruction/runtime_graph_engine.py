from __future__ import annotations

def build_runtime_graph(runtimes: list[str], services: list[str]):
    rs = sorted(set(runtimes or [])); sv = sorted(set(services or []))
    edges = [{"from": s, "to": r} for s in sv for r in rs]
    return {"nodes": sorted(set(rs + sv)), "edges": sorted(edges, key=lambda e: (e['from'], e['to']))}
