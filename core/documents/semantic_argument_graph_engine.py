from __future__ import annotations

from core.documents.semantic_discourse_graph_engine import build_semantic_discourse_graph


def build_semantic_argument_graph(text: str):
    return build_semantic_discourse_graph(text)
