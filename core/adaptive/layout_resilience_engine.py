from __future__ import annotations

from typing import Any, Dict, List

from core.adaptive.dom_similarity_engine import compute_dom_similarity


def assess_layout_resilience(
    before_nodes: List[Dict[str, Any]],
    after_nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    similarity = compute_dom_similarity(before_nodes, after_nodes)

    return {
        "resilient": similarity.get("score", 0.0) >= 0.3,
        "similarity": similarity,
        "bounded": True,
    }
