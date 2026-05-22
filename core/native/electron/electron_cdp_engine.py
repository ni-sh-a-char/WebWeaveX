from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_electron_cdp(
    target_url: str = "",
    devtools_port: int = 9222,
) -> Dict[str, Any]:
    """Chromium DevTools Protocol metadata (structural when CDP socket unavailable)."""
    endpoints = sorted(
        [
            {"method": "Runtime.evaluate", "domain": "Runtime"},
            {"method": "DOM.getDocument", "domain": "DOM"},
            {"method": "Network.enable", "domain": "Network"},
            {"method": "Page.navigate", "domain": "Page"},
        ],
        key=lambda e: e["method"],
    )
    return {
        "available": bool(target_url or devtools_port),
        "devtools_port": devtools_port,
        "target_url": target_url,
        "protocol": "cdp",
        "endpoints": endpoints,
        "preload_scripts": [],
        "bounded": True,
    }
