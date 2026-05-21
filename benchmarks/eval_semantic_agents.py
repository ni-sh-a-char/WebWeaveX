from __future__ import annotations

from typing import Any, Dict

from core.agents import route_semantic_capability


def eval_semantic_agents(case: Dict[str, Any]) -> Dict[str, Any]:
    r = route_semantic_capability(case["capability"], case["agents"])
    return {
        "predicted": r["selected"] == case["expected_selected"],
        "actual": {"selected": r["selected"]},
        "expected": case["expected_selected"],
    }
