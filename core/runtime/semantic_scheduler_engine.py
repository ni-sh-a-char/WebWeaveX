from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.runtime_budget_engine import DEFAULT_RUNTIME_BUDGET


def schedule_semantic_runtime_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(tasks, key=lambda t: (int(t.get("priority", 0)), str(t.get("id", ""))))
    bounded = ordered[: DEFAULT_RUNTIME_BUDGET.max_tasks]
    return {
        "scheduled": [{"id": t.get("id"), "priority": t.get("priority", 0)} for t in bounded],
        "dropped": max(0, len(ordered) - len(bounded)),
        "deterministic": True,
        "bounded": True,
    }
