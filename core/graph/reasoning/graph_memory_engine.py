from __future__ import annotations

from core.graph.graph_reconstruction_engine import bound_graph_memory


def graph_memory_bound(graph: dict, max_nodes: int = 5000, max_edges: int = 20000):
    return bound_graph_memory(graph, max_nodes=max_nodes, max_edges=max_edges)
