from __future__ import annotations

from typing import Any, Dict

from core.query.graph_scale_traversal_engine import (
    traverse_large_graph,
)


def eval_semantic_scale(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    r = traverse_large_graph(
        case["graph"],
        "a",
    )

    return {
        "predicted": (
            r["count"]
            == case["expected_count"]
        ),
        "expected_match": True,
    }
