from __future__ import annotations


def _unique_sorted(values):
    return sorted(set(str(v) for v in values if v))


def build_repository_knowledge(repo: dict):
    r = repo or {}
    nodes = _unique_sorted(
        (r.get("symbols", []) or [])
        + (r.get("dependencies", []) or [])
        + (r.get("frameworks", []) or [])
        + (r.get("services", []) or [])
    )
    edges = [{"from": nodes[i], "to": nodes[i + 1]} for i in range(max(0, len(nodes) - 1))]
    return {"nodes": nodes, "edges": edges}
