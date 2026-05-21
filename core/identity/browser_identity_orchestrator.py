from __future__ import annotations

from typing import Any, Dict

from core.identity.browser_entropy_engine import (
    compute_runtime_entropy,
    normalize_browser_fingerprint,
)
from core.identity.browser_fingerprint_engine import fingerprint_browser_identity
from core.identity.browser_profile_engine import build_browser_profile
from core.identity.canvas_runtime_engine import build_canvas_runtime
from core.identity.font_runtime_engine import build_font_runtime
from core.identity.language_runtime_engine import build_language_runtime
from core.identity.media_device_runtime_engine import build_media_device_runtime
from core.identity.navigator_runtime_engine import build_navigator_runtime
from core.identity.platform_runtime_engine import build_platform_runtime
from core.identity.timezone_runtime_engine import build_timezone_runtime
from core.identity.user_agent_runtime_engine import build_user_agent_runtime
from core.identity.webgl_runtime_engine import build_webgl_runtime

_SCREEN_PROFILES = {
    "default": {"width": 1920, "height": 1080, "colorDepth": 24},
    "profile_a": {"width": 1440, "height": 900, "colorDepth": 24},
    "profile_b": {"width": 2560, "height": 1440, "colorDepth": 24},
}


def build_browser_identity(
    profile_id: str = "default",
) -> Dict[str, Any]:
    profile = build_browser_profile(profile_id)
    bounded_id = profile["profile_id"]

    ua = build_user_agent_runtime(bounded_id)
    platform = build_platform_runtime(bounded_id)
    languages = build_language_runtime(bounded_id)
    timezone = build_timezone_runtime(bounded_id)
    webgl = build_webgl_runtime(bounded_id)
    canvas = build_canvas_runtime(bounded_id)
    fonts = build_font_runtime(bounded_id)
    media = build_media_device_runtime(bounded_id)
    navigator = build_navigator_runtime(bounded_id)

    identity = {
        "profile_id": bounded_id,
        "user_agent": ua["user_agent"],
        "platform": platform["platform"],
        "languages": languages["languages"],
        "timezone": timezone["timezone"],
        "screen": dict(_SCREEN_PROFILES.get(bounded_id, _SCREEN_PROFILES["default"])),
        "webgl": webgl,
        "fonts": fonts["fonts"],
        "media_devices": {
            "audio_inputs": media["audio_inputs"],
            "video_inputs": media["video_inputs"],
            "audio_outputs": media["audio_outputs"],
        },
        "canvas_fingerprint": canvas["canvas_fingerprint"],
        "navigator": navigator,
        "rotation_index": profile.get("rotation_index", 0),
        "bounded": True,
    }

    entropy = compute_runtime_entropy(identity)
    identity["entropy_profile"] = entropy["baseline_hash"]

    identity["fingerprint_hash"] = fingerprint_browser_identity(identity)

    return identity
