from __future__ import annotations

from typing import Any, Dict, List


def verify_runtime_consistency(
    history: Dict[str, Any],
    convergence: Dict[str, Any],
    replay: Dict[str, Any],
) -> Dict[str, Any]:
    deltas = list(history.get("deltas", []))
    issues: List[str] = []

    if not convergence.get("converged"):
        issues.append("convergence_incomplete")

    if not replay.get("replayed"):
        issues.append("replay_not_ready")

    for index in range(1, len(deltas)):
        if int(deltas[index].get("timestamp", 0)) < int(deltas[index - 1].get("timestamp", 0)):
            issues.append("timeline_order_violation")
            break

    return {
        "consistent": len(issues) == 0,
        "issues": issues,
        "synchronization_integrity": len(issues) == 0,
        "semantic_continuity": "semantic_evolution" in history,
        "replay_consistency": replay.get("replayed", False),
        "distributed_convergence": convergence.get("converged", False),
        "bounded": True,
    }
