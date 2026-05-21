from __future__ import annotations

from typing import Any, Dict

from core.world_model import build_semantic_architecture_graph


def eval_semantic_architecture(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_semantic_architecture_graph(case.get("repository_irs", []))
    edge_count = len(result.get("edges", []))
    pred = edge_count == case.get("expected_edge_count", 0)
    return {
        "predicted": pred,
        "actual": {"edge_count": edge_count},
        "expected": case.get("expected_edge_count"),
    }
