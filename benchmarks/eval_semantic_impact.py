from __future__ import annotations

from typing import Any, Dict

from core.world_model import analyze_semantic_impact


def eval_semantic_impact(case: Dict[str, Any]) -> Dict[str, Any]:
    result = analyze_semantic_impact(
        case.get("target", ""),
        case.get("graph", {}),
    )
    pred = result.get("impact_size") == case.get("expected_impact_size", 0)
    return {
        "predicted": pred,
        "actual": {"impact_size": result.get("impact_size")},
        "expected": case.get("expected_impact_size"),
    }
