from __future__ import annotations

from typing import Any, Dict

from core.query_language import parse_semantic_query


def eval_query_language(case: Dict[str, Any]) -> Dict[str, Any]:
    r = parse_semantic_query(case["query"])
    return {
        "predicted": r["limit"] == case["expected_limit"],
        "actual": {"limit": r["limit"]},
        "expected": case["expected_limit"],
    }
