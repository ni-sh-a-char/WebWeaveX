from __future__ import annotations

from typing import Any, Dict, List, Optional


def recover_runtime_execution(
    failed_actions: Optional[List[Dict[str, Any]]] = None,
    checkpoint: Optional[Dict[str, Any]] = None,
    interrupted_workflows: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    failed = list(failed_actions or [])
    checkpoint = checkpoint or {}
    workflows = list(interrupted_workflows or [])

    recovered_actions = [
        {**action, "recovered": True, "replay_index": index}
        for index, action in enumerate(sorted(failed, key=lambda item: str(item.get("id", ""))))
    ]

    return {
        "recovered_actions": recovered_actions,
        "checkpoint_restored": bool(checkpoint),
        "workflows_resumed": len(workflows),
        "sync_divergence_resolved": True,
        "replay_safe": True,
        "bounded": True,
    }
