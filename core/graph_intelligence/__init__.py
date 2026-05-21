"""Shim — use core.graph."""
from core.graph import (
    compress_graph,
    export_graph,
    query_edges,
    query_nodes,
    reason_topology,
    reconstruct_graph,
)
from core.graph.topology_reasoning_engine import reason_topology as graph_reasoning
from core.graph.graph_reconstruction_engine import reconstruct_graph as graph_clustering

graph_similarity = reason_topology
__all__ = ["graph_reasoning", "graph_similarity", "graph_clustering", "reconstruct_graph"]
