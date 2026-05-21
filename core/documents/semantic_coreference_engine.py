from __future__ import annotations

from core.documents.coreference_graph_engine import build_coreference_graph


def resolve_semantic_coreference(text: str):
    return build_coreference_graph(text)
