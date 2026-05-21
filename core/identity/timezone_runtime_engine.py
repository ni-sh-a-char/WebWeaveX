from __future__ import annotations

from typing import Any, Dict

_TIMEZONES = {
    "default": "America/New_York",
    "profile_a": "Europe/London",
    "profile_b": "America/Los_Angeles",
}


def build_timezone_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _TIMEZONES else "default"

    return {
        "timezone": _TIMEZONES[profile],
        "bounded": True,
    }
