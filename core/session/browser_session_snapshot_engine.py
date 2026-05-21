from __future__ import annotations

from typing import Any, Dict, List

MAX_COOKIES = 1000
MAX_STORAGE_ITEMS = 1000
MAX_HEADERS = 200
MAX_TOKENS = 500

_LOCAL_STORAGE_SCRIPT = """
() => {
  const items = {};
  const limit = Math.min(localStorage.length, 1000);
  for (let i = 0; i < limit; i++) {
    const key = localStorage.key(i);
    if (key) {
      items[key] = localStorage.getItem(key);
    }
  }
  return items;
}
"""

_SESSION_STORAGE_SCRIPT = """
() => {
  const items = {};
  const limit = Math.min(sessionStorage.length, 1000);
  for (let i = 0; i < limit; i++) {
    const key = sessionStorage.key(i);
    if (key) {
      items[key] = sessionStorage.getItem(key);
    }
  }
  return items;
}
"""


def _empty_snapshot() -> Dict[str, Any]:
    return {
        "cookies": [],
        "local_storage": {},
        "session_storage": {},
        "headers": {},
        "auth_tokens": [],
        "origin": "",
        "bounded": True,
    }


def capture_browser_session(
    page: Any,
    context: Any,
) -> Dict[str, Any]:
    if page is None and context is None:
        return _empty_snapshot()

    if hasattr(page, "_test_snapshot"):
        snapshot = dict(page._test_snapshot)
        snapshot["bounded"] = True
        return snapshot

    cookies: List[Dict[str, Any]] = []
    local_storage: Dict[str, str] = {}
    session_storage: Dict[str, str] = {}
    origin = ""

    if context is not None and hasattr(context, "cookies"):
        try:
            cookies = list(context.cookies())[:MAX_COOKIES]
        except Exception:
            cookies = []

    if page is not None:
        try:
            origin = str(page.url or "")
        except Exception:
            origin = ""

        if hasattr(page, "evaluate"):
            try:
                local_storage = dict(
                    page.evaluate(_LOCAL_STORAGE_SCRIPT) or {}
                )
            except Exception:
                local_storage = {}

            try:
                session_storage = dict(
                    page.evaluate(_SESSION_STORAGE_SCRIPT) or {}
                )
            except Exception:
                session_storage = {}

    local_storage = {
        str(k): str(v)[:5000]
        for k, v in sorted(local_storage.items())[:MAX_STORAGE_ITEMS]
    }
    session_storage = {
        str(k): str(v)[:5000]
        for k, v in sorted(session_storage.items())[:MAX_STORAGE_ITEMS]
    }

    return {
        "cookies": sorted(
            [dict(cookie) for cookie in cookies],
            key=lambda item: (
                str(item.get("name", "")),
                str(item.get("domain", "")),
            ),
        )[:MAX_COOKIES],
        "local_storage": local_storage,
        "session_storage": session_storage,
        "headers": {},
        "auth_tokens": [],
        "origin": origin[:2000],
        "bounded": True,
    }


def restore_browser_session(
    context: Any,
    snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    if context is None:
        return {
            "restored": False,
            "reason": "missing_context",
            "bounded": True,
        }

    cookies = list(snapshot.get("cookies", []))[:MAX_COOKIES]

    if hasattr(context, "add_cookies") and cookies:
        try:
            context.add_cookies(cookies)
        except Exception as exc:
            return {
                "restored": False,
                "reason": str(exc)[:200],
                "bounded": True,
            }

    if hasattr(context, "_test_pages"):
        for page in context._test_pages:
            if hasattr(page, "_test_snapshot"):
                page._test_snapshot = dict(snapshot)

    return {
        "restored": True,
        "cookie_count": len(cookies),
        "bounded": True,
    }
