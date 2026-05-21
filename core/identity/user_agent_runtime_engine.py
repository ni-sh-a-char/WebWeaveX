from __future__ import annotations

from typing import Any, Dict

_USER_AGENTS = {
    "default": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "profile_a": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "profile_b": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def build_user_agent_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _USER_AGENTS else "default"

    return {
        "user_agent": _USER_AGENTS[profile],
        "bounded": True,
    }
