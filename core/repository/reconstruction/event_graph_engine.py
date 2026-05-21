from __future__ import annotations

def build_event_graph(text: str):
    src = (text or '').lower()
    producers = sorted(set([k for k in ['publish', 'emit', 'producer', 'kafka', 'sns'] if k in src]))
    consumers = sorted(set([k for k in ['consume', 'subscriber', 'handler', 'worker', 'sqs'] if k in src]))
    nodes = sorted(set(producers + consumers))
    edges = [{"from": p, "to": c} for p in producers for c in consumers[:5]]
    return {"nodes": nodes, "edges": sorted(edges, key=lambda e: (e['from'], e['to']))}
