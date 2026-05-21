from __future__ import annotations

from typing import Any, Dict

from core.database.semantic_index_engine import SemanticIndex


def eval_database_kernel(case: Dict[str, Any]) -> Dict[str, Any]:
    index = SemanticIndex()
    index.insert(case["key"], case["value"])
    count = len(index.lookup(case["key"]))
    return {
        "predicted": count == case["expected_count"],
        "actual": {"count": count},
        "expected": case["expected_count"],
    }
