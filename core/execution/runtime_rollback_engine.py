from __future__ import annotations

from typing import Any, Dict, Optional


def restore_runtime_checkpoint(
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "browser": dict(checkpoint.get("browser", {})),
        "interaction": dict(checkpoint.get("interaction", {})),
        "native": dict(checkpoint.get("native", {})),
        "workflow": dict(checkpoint.get("workflow", {})),
        "synchronization": dict(checkpoint.get("synchronization", {})),
        "memory": dict(checkpoint.get("memory", {})),
        "restored": True,
        "bounded": True,
    }


def rollback_runtime_state(
    prior: Dict[str, Any],
    current: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    restored = restore_runtime_checkpoint(prior)
    return {
        "prior": prior,
        "current": current or {},
        "restored_state": restored,
        "rolled_back": True,
        "replay_safe": True,
        "bounded": True,
    }
