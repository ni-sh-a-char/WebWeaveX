from __future__ import annotations

from typing import Any, Dict, List

MAX_NODES = 10000


def _node_signature(node: Dict[str, Any]) -> str:
    return "|".join([
        str(node.get("tag", "")),
        str(node.get("text", ""))[:200],
        str(node.get("depth", 0)),
    ])


def compute_dom_similarity(
    left_nodes: List[Dict[str, Any]],
    right_nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    left = left_nodes[:MAX_NODES]
    right = right_nodes[:MAX_NODES]

    left_sigs = [_node_signature(node) for node in left]
    right_sigs = [_node_signature(node) for node in right]

    left_set = set(left_sigs)
    right_set = set(right_sigs)

    overlap = len(left_set & right_set)
    union = max(len(left_set | right_set), 1)

    return {
        "score": overlap / union,
        "overlap": overlap,
        "left_count": len(left),
        "right_count": len(right),
        "bounded": True,
    }
