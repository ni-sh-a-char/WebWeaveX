from __future__ import annotations

from typing import Any, Dict

from core.identity.browser_entropy_engine import normalize_browser_fingerprint
from core.identity.navigator_runtime_engine import build_navigator_runtime


def replay_browser_identity(
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    profile_id = str(identity.get("profile_id", "default"))
    navigator = build_navigator_runtime(profile_id)

    restored = {
        **identity,
        "navigator": navigator,
        "user_agent": identity.get("user_agent", navigator["user_agent"]),
        "platform": identity.get("platform", navigator["platform"]),
        "languages": identity.get("languages", navigator["languages"]),
        "timezone": identity.get("timezone", identity.get("timezone", "UTC")),
        "canvas_fingerprint": identity.get("canvas_fingerprint", ""),
        "entropy_profile": identity.get("entropy_profile", ""),
    }

    return {
        "identity": restored,
        "normalized": normalize_browser_fingerprint(restored),
        "replayed": True,
        "bounded": True,
    }
