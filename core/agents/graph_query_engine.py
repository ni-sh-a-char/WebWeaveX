from __future__ import annotations


def query_nodes(graph: dict, node: str = ""):
    nodes = graph.get("nodes", [])
    if not node:
        return nodes
    return [n for n in nodes if node in str(n.get("id", ""))]


def query_edges(graph: dict, node: str = ""):
    edges = graph.get("edges", [])
    if not node:
        return edges
    return [e for e in edges if node in e.get("from", "") or node in e.get("to", "")]


def query_dependencies(result: dict):
    return result.get("dependencies", {})


def query_services(result: dict):
    return result.get("repository", {}).get("services", [])

