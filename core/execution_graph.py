"""Deterministic structural graph reconstruction."""

from __future__ import annotations

from typing import Any, Dict, List

from core.graph.graph_reconstruction_engine import MAX_EDGES as MAX_EDGES_V3
from core.graph.graph_reconstruction_engine import MAX_NODES, reconstruct_graph

MAX_EDGES = 500


def build_execution_graph(
    system_graph: Dict[str, Any],
    max_edges: int = MAX_EDGES,
    max_nodes: int = MAX_NODES,
) -> Dict[str, Any]:
    return reconstruct_graph(system_graph, max_edges=max_edges, max_nodes=max_nodes)


def infer_execution_order(system_graph: Dict[str, Any]) -> List[str]:
    graph = build_execution_graph(system_graph)
    return [n["id"] for n in graph["nodes"]]


def build_execution_graph_v3(system_graph: Dict[str, Any]) -> Dict[str, Any]:
    return reconstruct_graph(system_graph, max_edges=MAX_EDGES_V3, max_nodes=MAX_NODES)
