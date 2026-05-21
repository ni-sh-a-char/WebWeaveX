from __future__ import annotations

from .graph_reconstruction_engine import MAX_EDGES, reconstruct_graph


def compress_graph(graph: dict, max_edges: int = MAX_EDGES) -> dict:
    rebuilt = reconstruct_graph(graph, max_edges=max_edges)
    return rebuilt
