from __future__ import annotations

from typing import Any, Dict

from core.query.semantic_query_execution_engine import execute_semantic_query


def eval_query_execution(case: Dict[str, Any]) -> Dict[str, Any]:
    r = execute_semantic_query(
        nodes=case.get("nodes", []),
        filters=case.get("filters", {}),
    )
    return {
        "predicted": r["count"] == case.get("expected_count", 0),
        "actual": {"count": r["count"]},
        "expected": case.get("expected_count"),
    }
