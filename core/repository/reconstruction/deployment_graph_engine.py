from __future__ import annotations

def build_deployment_graph(text: str):
    src = (text or '').lower()
    nodes = []
    for k in ['docker', 'kubernetes', 'helm', 'terraform', 'github actions', 'gitlab-ci']:
        if k in src:
            nodes.append(k)
    n = sorted(set(nodes))
    edges = [{"from": n[i], "to": n[i+1]} for i in range(max(0, len(n)-1))]
    return {"nodes": n, "edges": edges}
