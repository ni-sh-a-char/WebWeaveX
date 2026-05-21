from __future__ import annotations

def classify_architecture(topology: dict, event_graph: dict, deployment: dict):
    styles = ['monolith']
    if len(topology.get('services', [])) >= 5:
        styles.append('microservices')
    if len(event_graph.get('edges', [])) > 0:
        styles.append('event-driven')
    if any('kubernetes' in n for n in deployment.get('nodes', [])):
        styles.append('distributed')
    return {"styles": sorted(set(styles))}
