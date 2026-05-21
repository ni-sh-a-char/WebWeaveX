from __future__ import annotations

from typing import Any, Dict, List

_FONTS = {
    "default": [
        "Arial",
        "Courier New",
        "Segoe UI",
        "Times New Roman",
        "Verdana",
    ],
    "profile_a": [
        "Arial",
        "Helvetica",
        "Menlo",
        "Times New Roman",
    ],
    "profile_b": [
        "DejaVu Sans",
        "Liberation Sans",
        "Ubuntu",
        "Noto Sans",
    ],
}


def build_font_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _FONTS else "default"

    return {
        "fonts": sorted(_FONTS[profile]),
        "bounded": True,
    }
