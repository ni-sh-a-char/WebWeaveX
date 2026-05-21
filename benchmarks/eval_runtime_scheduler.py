from __future__ import annotations

from typing import Any, Dict

from core.runtime.semantic_resource_scheduler import schedule_semantic_resources


def eval_runtime_scheduler(case: Dict[str, Any]) -> Dict[str, Any]:
    r = schedule_semantic_resources(case["tasks"])
    first = r["scheduled"][0]["id"] if r["scheduled"] else None
    return {
        "predicted": first == case["expected_first"],
        "actual": {"first": first},
        "expected": case["expected_first"],
    }
