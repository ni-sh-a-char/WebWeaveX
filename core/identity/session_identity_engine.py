from __future__ import annotations

from typing import Any, Dict


def attach_identity_to_session(
    session: Dict[str, Any],
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(session)
    merged["browser_identity"] = dict(identity)
    merged["identity_attached"] = True
    merged["bounded"] = True
    return merged


def restore_identity_session(
    session: Dict[str, Any],
) -> Dict[str, Any]:
    identity = dict(session.get("browser_identity", {}))

    return {
        "session": session,
        "identity": identity,
        "restored": bool(identity),
        "bounded": True,
    }
