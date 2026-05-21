from __future__ import annotations

from typing import Any, Dict, List

from core.internet.semantic_propagation_engine import model_semantic_propagation


def analyze_information_diffusion(seed: str, graph_edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    return model_semantic_propagation(seed, graph_edges)
