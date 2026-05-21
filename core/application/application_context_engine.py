from __future__ import annotations

from typing import Any, Dict


def build_application_context(
    url: str,
    state: Dict[str, Any],
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "url": url,
        "route": state.get("route", url),
        "authenticated": state.get("authenticated", False),
        "identity_profile": identity.get("profile_id", "default"),
        "bounded": True,
    }
