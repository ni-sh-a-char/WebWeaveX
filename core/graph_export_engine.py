from __future__ import annotations
from core.serialize.deterministic_serializer import dumps_deterministic

def export_graph(graph: dict):
    return dumps_deterministic(graph)
