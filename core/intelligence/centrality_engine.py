"""Centrality Engine - Node importance ranking."""


def compute_centrality(nodes, edges):
    degree = {}

    for node in nodes:
        node_id = node.get("id", "")
        if node_id:
            degree[node_id] = {"in": 0, "out": 0}

    for edge in edges:
        f = edge.get("from", "")
        t = edge.get("to", "")

        if f in degree:
            degree[f]["out"] += 1
        if t in degree:
            degree[t]["in"] += 1

    scored = []
    for node, d in degree.items():
        score = d["in"] + d["out"]
        scored.append((node, score))

    ranked = sorted(scored, key=lambda x: (-x[1], x[0]))

    return [
        {"id": node, "score": score}
        for node, score in ranked
    ]