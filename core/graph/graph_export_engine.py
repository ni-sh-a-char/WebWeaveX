from __future__ import annotations

from core.serialize.deterministic_serializer import dumps_deterministic

from .graph_reconstruction_engine import normalize_graph_nodes


def export_graph(graph: dict) -> str:
    normalized = normalize_graph_nodes(graph if isinstance(graph, dict) else {})
    return dumps_deterministic(normalized)
