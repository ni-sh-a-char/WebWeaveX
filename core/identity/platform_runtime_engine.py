from __future__ import annotations

from typing import Any, Dict

_PLATFORMS = {
    "default": "Win32",
    "profile_a": "MacIntel",
    "profile_b": "Linux x86_64",
}


def build_platform_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _PLATFORMS else "default"

    return {
        "platform": _PLATFORMS[profile],
        "bounded": True,
    }
