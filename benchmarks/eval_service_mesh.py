from __future__ import annotations

from typing import Any, Dict

from core.distributed import build_semantic_service_mesh


def eval_service_mesh(case: Dict[str, Any]) -> Dict[str, Any]:
    r = build_semantic_service_mesh(case["services"])
    return {
        "predicted": len(r["links"]) == case["expected_links"],
        "actual": {"links": len(r["links"])},
        "expected": case["expected_links"],
    }
