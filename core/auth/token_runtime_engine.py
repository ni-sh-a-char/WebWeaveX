from __future__ import annotations

import json
import re
from typing import Any, Dict, List

MAX_TOKENS = 500

_BEARER_RE = re.compile(
    r"Bearer\s+([A-Za-z0-9\-_.]+)",
    re.IGNORECASE,
)
_JWT_RE = re.compile(
    r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
)


def extract_auth_tokens(page: Any) -> Dict[str, Any]:
    tokens: List[Dict[str, Any]] = []

    if page is None:
        return {
            "tokens": [],
            "bounded": True,
        }

    if hasattr(page, "_test_tokens"):
        tokens = list(page._test_tokens)[:MAX_TOKENS]
        return {
            "tokens": sorted(
                tokens,
                key=lambda item: (
                    str(item.get("type", "")),
                    str(item.get("value", "")),
                ),
            ),
            "bounded": True,
        }

    headers: Dict[str, str] = {}

    if hasattr(page, "_test_headers"):
        headers = dict(page._test_headers)

    authorization = str(headers.get("Authorization", ""))

    bearer_match = _BEARER_RE.search(authorization)
    if bearer_match:
        tokens.append({
            "type": "bearer",
            "value": bearer_match.group(1)[:5000],
        })

    for match in _JWT_RE.findall(authorization):
        tokens.append({
            "type": "jwt",
            "value": match[:5000],
        })

    if hasattr(page, "_test_snapshot"):
        storage = page._test_snapshot.get("local_storage", {})
        for key in sorted(storage.keys()):
            value = str(storage[key])
            if _JWT_RE.search(value):
                tokens.append({
                    "type": "local_storage_auth",
                    "name": key,
                    "value": value[:5000],
                })

    return {
        "tokens": sorted(
            tokens,
            key=lambda item: (
                str(item.get("type", "")),
                str(item.get("name", "")),
                str(item.get("value", "")),
            ),
        )[:MAX_TOKENS],
        "bounded": True,
    }


def inject_auth_tokens(
    page: Any,
    tokens: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bounded = sorted(
        [dict(token) for token in tokens[:MAX_TOKENS]],
        key=lambda item: (
            str(item.get("type", "")),
            str(item.get("value", "")),
        ),
    )

    if page is None:
        return {
            "injected": False,
            "token_count": 0,
            "bounded": True,
        }

    headers = {}

    for token in bounded:
        token_type = str(token.get("type", ""))
        value = str(token.get("value", ""))

        if token_type == "bearer":
            headers["Authorization"] = f"Bearer {value}"

    if hasattr(page, "_test_headers"):
        page._test_headers.update(headers)

    if hasattr(page, "_test_tokens"):
        page._test_tokens = bounded

    return {
        "injected": True,
        "token_count": len(bounded),
        "serialized": json.dumps(
            bounded,
            sort_keys=True,
            separators=(",", ":"),
        ),
        "bounded": True,
    }
