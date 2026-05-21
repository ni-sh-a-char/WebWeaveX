from __future__ import annotations

from typing import Any, Dict

from core.auth.cookie_runtime_engine import inject_cookies
from core.auth.token_runtime_engine import inject_auth_tokens
from core.session.browser_session_snapshot_engine import (
    restore_browser_session,
)


def restore_authenticated_session(
    context: Any,
    page: Any,
    session: Dict[str, Any],
) -> Dict[str, Any]:
    snapshot = {
        "cookies": list(session.get("cookies", [])),
        "local_storage": dict(session.get("local_storage", {})),
        "session_storage": dict(session.get("session_storage", {})),
        "headers": dict(session.get("headers", {})),
        "auth_tokens": list(session.get("auth_tokens", [])),
        "origin": str(session.get("origin", "")),
        "bounded": True,
    }

    restored = restore_browser_session(context, snapshot)
    inject_cookies(context, snapshot["cookies"])
    inject_auth_tokens(page, list(session.get("auth_tokens", [])))

    if page is not None and hasattr(page, "_test_headers"):
        page._test_headers.update(dict(session.get("headers", {})))

    return {
        **restored,
        "headers_applied": len(session.get("headers", {})),
        "bounded": True,
    }
