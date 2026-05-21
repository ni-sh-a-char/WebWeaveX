from __future__ import annotations

from typing import Any, Dict, Optional


def capture_runtime_snapshot(
    browser: Optional[Dict[str, Any]] = None,
    native: Optional[Dict[str, Any]] = None,
    semantic: Optional[Dict[str, Any]] = None,
    workflow: Optional[Dict[str, Any]] = None,
    causality: Optional[Dict[str, Any]] = None,
    sync_state: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    return {
        "snapshot_id": f"snapshot:{tick}",
        "tick": tick,
        "browser_runtime": dict(browser or {}),
        "native_runtime": dict(native or {}),
        "semantic_runtime": dict(semantic or {}),
        "workflow_state": dict(workflow or {}),
        "causality_state": dict(causality or {}),
        "synchronization_state": dict(sync_state or {}),
        "bounded": True,
    }
