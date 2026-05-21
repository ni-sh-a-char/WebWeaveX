from __future__ import annotations

from typing import Any, Dict, List

from core.identity.language_runtime_engine import build_language_runtime
from core.identity.platform_runtime_engine import build_platform_runtime
from core.identity.user_agent_runtime_engine import build_user_agent_runtime


def build_navigator_runtime(profile_id: str = "default") -> Dict[str, Any]:
    ua = build_user_agent_runtime(profile_id)
    platform = build_platform_runtime(profile_id)
    languages = build_language_runtime(profile_id)

    return {
        "webdriver": False,
        "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer"],
        "mimeTypes": ["application/pdf"],
        "hardwareConcurrency": 8,
        "deviceMemory": 8,
        "languages": languages["languages"],
        "permissions": {
            "notifications": "default",
            "geolocation": "prompt",
        },
        "user_agent": ua["user_agent"],
        "platform": platform["platform"],
        "bounded": True,
    }
