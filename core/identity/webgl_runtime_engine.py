from __future__ import annotations

from typing import Any, Dict, List

_WEBGL = {
    "default": {
        "vendor": "Google Inc. (Intel)",
        "renderer": "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "extensions": ["WEBGL_debug_renderer_info", "OES_texture_float"],
    },
    "profile_a": {
        "vendor": "Apple Inc.",
        "renderer": "Apple GPU",
        "extensions": ["WEBGL_debug_renderer_info"],
    },
    "profile_b": {
        "vendor": "Google Inc. (NVIDIA)",
        "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060)",
        "extensions": ["WEBGL_debug_renderer_info", "EXT_texture_filter_anisotropic"],
    },
}


def build_webgl_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _WEBGL else "default"
    data = _WEBGL[profile]

    return {
        "vendor": data["vendor"],
        "renderer": data["renderer"],
        "extensions": sorted(data["extensions"]),
        "bounded": True,
    }
