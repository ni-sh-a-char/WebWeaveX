from __future__ import annotations

import re
from typing import Any, Dict, List

MAX_CSRF = 200

_META_RE = re.compile(
    r'<meta[^>]+name=["\']csrf-token["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_INPUT_RE = re.compile(
    r'<input[^>]+name=["\']([^"\']*csrf[^"\']*)["\'][^>]+value=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def extract_csrf_tokens(page: Any) -> Dict[str, Any]:
    tokens: List[Dict[str, Any]] = []

    html = ""

    if page is None:
        return {
            "tokens": [],
            "bounded": True,
        }

    if hasattr(page, "_test_html"):
        html = str(page._test_html)
    elif hasattr(page, "_test_snapshot"):
        html = str(page._test_snapshot.get("html", ""))

    for match in _META_RE.findall(html)[:MAX_CSRF]:
        tokens.append({
            "source": "meta",
            "value": match[:2000],
        })

    for name, value in _INPUT_RE.findall(html)[:MAX_CSRF]:
        tokens.append({
            "source": "hidden_input",
            "name": name[:200],
            "value": value[:2000],
        })

    headers = getattr(page, "_test_headers", {})
    for header_name in sorted(headers.keys()):
        if "csrf" in header_name.lower():
            tokens.append({
                "source": "header",
                "name": header_name,
                "value": str(headers[header_name])[:2000],
            })

    return {
        "tokens": sorted(
            tokens,
            key=lambda item: (
                str(item.get("source", "")),
                str(item.get("name", "")),
                str(item.get("value", "")),
            ),
        )[:MAX_CSRF],
        "bounded": True,
    }
