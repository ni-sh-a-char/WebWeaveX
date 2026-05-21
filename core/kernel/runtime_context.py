from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_context(
    runtime_type: str = "browser",
    tick: int = 0,
    sources: Optional[Dict[str, Any]] = None,
    policy: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    sources = sources or {}
    return {
        "runtime_type": runtime_type,
        "tick": tick,
        "sources": dict(sources),
        "policy": dict(policy or {}),
        "phase_state": {},
        "bounded": True,
    }
