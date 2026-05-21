from __future__ import annotations

from core.repository.dependency_graph_engine import build_dependency_graph


def extract_dependencies_v2(text: str):
    return build_dependency_graph(text)
