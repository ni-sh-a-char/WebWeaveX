from __future__ import annotations

from typing import Any, Dict

from core.identity.browser_fingerprint_engine import fingerprint_browser_identity


def build_runtime_identity(
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "runtime_identity": fingerprint_browser_identity(identity),
        "profile_id": identity.get("profile_id", "default"),
        "bounded": True,
    }
