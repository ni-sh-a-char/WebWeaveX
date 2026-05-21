from __future__ import annotations

from typing import Any, Dict, Optional


def reconstruct_runtime_session(
    session: Optional[Dict[str, Any]] = None,
    identity: Optional[Dict[str, Any]] = None,
    sync_state: Optional[Dict[str, Any]] = None,
    adaptive_memory: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    session = session or {}
    identity = identity or {}
    sync_state = sync_state or {}
    adaptive_memory = adaptive_memory or {}

    cookies = sorted(session.get("cookies", []), key=lambda c: str(c.get("name", "")))

    return {
        "authenticated_session": {
            "authenticated": bool(session.get("authenticated", False)),
            "session_id": str(session.get("session_id", identity.get("identity_id", ""))),
        },
        "cookies": cookies,
        "csrf_state": dict(session.get("csrf", session.get("csrf_state", {}))),
        "browser_identity": dict(identity),
        "synchronization_state": dict(sync_state),
        "adaptive_memory": dict(adaptive_memory),
        "replay_safe": True,
        "bounded": True,
    }
