from __future__ import annotations

from typing import Any, Dict

from core.distributed import execute_semantic_dag


def eval_distributed_dag(case: Dict[str, Any]) -> Dict[str, Any]:
    r = execute_semantic_dag(case["nodes"])
    order = r.get("execution_order", [])
    return {
        "predicted": order == case["expected_order"],
        "actual": {"order": order},
        "expected": case["expected_order"],
    }
