from __future__ import annotations


def trace_paths(graph: dict, start: str):
    return [e for e in graph.get("edges", []) if e.get("from") == start]

