from __future__ import annotations

from typing import Any, Dict, List, Optional


def evolve_workflow_runtime(
    plan: Optional[Dict[str, Any]] = None,
    execution: Optional[Dict[str, Any]] = None,
    history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    plan = plan or {}
    execution = execution or {}
    history = history or []
    steps = list(plan.get("steps", []))

    score = len(execution.get("executed", []))
    optimized_steps = sorted(
        steps,
        key=lambda item: (
            -int(item.get("priority", 0)),
            str(item.get("id", "")),
        ),
    )

    return {
        "execution_ordering": [s.get("id", "") for s in optimized_steps],
        "retries": min(len(history), 3),
        "pacing": max(0, len(steps) - score),
        "sync_timing": len(steps),
        "recovery_ordering": ["retry_step", "realign_runtime", "checkpoint"],
        "score": score,
        "bounded": True,
    }
