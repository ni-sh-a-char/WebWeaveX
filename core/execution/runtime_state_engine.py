from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_execution_state(
    runtime: str = "browser",
    active_actions: Optional[List[Dict[str, Any]]] = None,
    queue: Optional[List[Dict[str, Any]]] = None,
    mutations: Optional[List[Dict[str, Any]]] = None,
    checkpoint: Optional[Dict[str, Any]] = None,
    transaction: Optional[Dict[str, Any]] = None,
    federation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "current_runtime": runtime,
        "active_actions": list(active_actions or []),
        "pending_queues": list(queue or []),
        "mutations": list(mutations or []),
        "checkpoint": dict(checkpoint or {}),
        "transaction": dict(transaction or {}),
        "federation_state": dict(federation or {}),
        "bounded": True,
    }
