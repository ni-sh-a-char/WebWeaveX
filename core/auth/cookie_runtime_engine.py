from __future__ import annotations

import json
from typing import Any, Dict, List


MAX_COOKIES = 1000


def extract_cookies(context: Any) -> Dict[str, Any]:
    if context is None:
        return {
            "cookies": [],
            "bounded": True,
        }

    if hasattr(context, "_test_cookies"):
        cookies = list(context._test_cookies)
    elif hasattr(context, "cookies"):
        try:
            cookies = list(context.cookies())
        except Exception:
            cookies = []
    else:
        cookies = []

    normalized = sorted(
        [dict(cookie) for cookie in cookies[:MAX_COOKIES]],
        key=lambda item: (
            str(item.get("name", "")),
            str(item.get("domain", "")),
            str(item.get("path", "")),
        ),
    )

    return {
        "cookies": normalized,
        "bounded": True,
    }


def inject_cookies(
    context: Any,
    cookies: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bounded = sorted(
        [dict(cookie) for cookie in cookies[:MAX_COOKIES]],
        key=lambda item: (
            str(item.get("name", "")),
            str(item.get("domain", "")),
        ),
    )

    if context is None:
        return {
            "injected": False,
            "cookie_count": 0,
            "bounded": True,
        }

    if hasattr(context, "add_cookies") and bounded:
        context.add_cookies(bounded)

    if hasattr(context, "_test_cookies"):
        context._test_cookies = bounded

    return {
        "injected": True,
        "cookie_count": len(bounded),
        "serialized": json.dumps(
            bounded,
            sort_keys=True,
            separators=(",", ":"),
        ),
        "bounded": True,
    }
