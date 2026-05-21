from __future__ import annotations

from typing import Any, Dict

from core.distributed import schedule_distributed_execution


def eval_distributed_execution(case: Dict[str, Any]) -> Dict[str, Any]:
    r = schedule_distributed_execution(
        tasks=case.get("tasks", []),
        nodes=case.get("nodes", []),
    )
    count = len(r.get("scheduled", []))
    return {
        "predicted": count == case.get("expected_scheduled", 0),
        "actual": {"count": count},
        "expected": case.get("expected_scheduled"),
    }
