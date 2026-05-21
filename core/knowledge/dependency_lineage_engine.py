from __future__ import annotations


def build_dependency_lineage(dependencies: list):
    ordered = sorted(set(dependencies or []))
    edges = [{"from": ordered[i], "to": ordered[i + 1]} for i in range(max(0, len(ordered) - 1))]
    return {"nodes": ordered, "edges": edges}
