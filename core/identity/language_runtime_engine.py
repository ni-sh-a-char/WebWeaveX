from __future__ import annotations

from typing import Any, Dict, List

_LANGUAGES = {
    "default": ["en-US", "en"],
    "profile_a": ["en-GB", "en"],
    "profile_b": ["en-US", "en"],
}


def build_language_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _LANGUAGES else "default"

    return {
        "languages": list(_LANGUAGES[profile]),
        "bounded": True,
    }
