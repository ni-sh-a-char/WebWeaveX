from __future__ import annotations

def run_gql(graph: dict, query: str):
    q=(query or '').strip().lower()
    if q=='nodes': return graph.get('nodes',[])
    if q=='edges': return graph.get('edges',[])
    return []
