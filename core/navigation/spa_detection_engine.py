from __future__ import annotations

import re
from typing import Any, Dict

_SPA_MARKERS = (
    "react",
    "vue",
    "angular",
    "__NEXT_DATA__",
    "history.pushState",
    "hashchange",
)


def detect_single_page_application(page: Any) -> Dict[str, Any]:
    html = ""

    if page is not None:
        if hasattr(page, "_test_spa_markers"):
            markers = list(page._test_spa_markers)
            return {
                "spa": len(markers) > 0,
                "markers": sorted(markers),
                "history_api": "history.pushState" in markers,
                "hash_routing": "hashchange" in markers,
                "bounded": True,
            }

        if hasattr(page, "_test_html"):
            html = str(page._test_html).lower()

    markers = []

    for marker in _SPA_MARKERS:
        if marker.lower() in html:
            markers.append(marker)

    history_api = bool(
        re.search(r"history\.pushstate", html, re.IGNORECASE)
    )
    hash_routing = "#/" in html or "hashchange" in html

    return {
        "spa": bool(markers) or history_api or hash_routing,
        "markers": sorted(set(markers)),
        "history_api": history_api,
        "hash_routing": hash_routing,
        "bounded": True,
    }
