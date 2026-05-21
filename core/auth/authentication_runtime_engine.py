from __future__ import annotations

from typing import Any, Dict

from core.auth.cookie_runtime_engine import inject_cookies
from core.auth.token_runtime_engine import inject_auth_tokens


MAX_LOGIN_STEPS = 100


def authenticate_runtime(
    page: Any,
    credentials: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    method = str(config.get("method", "cookie_injection")).strip()

    if page is None:
        return {
            "authenticated": False,
            "method": method,
            "reason": "missing_page",
            "bounded": True,
        }

    context = getattr(page, "context", None)

    if method == "form_login":
        username_selector = str(
            config.get("username_selector", "#username")
        )
        password_selector = str(
            config.get("password_selector", "#password")
        )
        submit_selector = str(
            config.get("submit_selector", "button[type='submit']")
        )

        if hasattr(page, "fill") and hasattr(page, "click"):
            page.fill(
                username_selector,
                str(credentials.get("username", ""))[:500],
            )
            page.fill(
                password_selector,
                str(credentials.get("password", ""))[:500],
            )
            page.click(submit_selector)

        return {
            "authenticated": True,
            "method": method,
            "bounded": True,
        }

    if method == "cookie_injection":
        cookies = list(credentials.get("cookies", []))
        inject_cookies(context, cookies)

        return {
            "authenticated": True,
            "method": method,
            "cookie_count": len(cookies),
            "bounded": True,
        }

    if method == "token_injection":
        tokens = list(credentials.get("tokens", []))
        inject_auth_tokens(page, tokens)

        return {
            "authenticated": True,
            "method": method,
            "token_count": len(tokens),
            "bounded": True,
        }

    if method == "persistent_auth_replay":
        session = dict(credentials.get("session", {}))
        inject_cookies(context, list(session.get("cookies", [])))
        inject_auth_tokens(page, list(session.get("auth_tokens", [])))

        return {
            "authenticated": True,
            "method": method,
            "bounded": True,
        }

    return {
        "authenticated": False,
        "method": method,
        "reason": "unsupported_method",
        "bounded": True,
    }


def rotate_authenticated_session(
    session: Dict[str, Any],
) -> Dict[str, Any]:
    rotated = dict(session)
    rotated["rotation_index"] = int(
        session.get("rotation_index", 0)
    ) + 1
    rotated["authenticated"] = True
    rotated["bounded"] = True

    return rotated
