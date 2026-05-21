from __future__ import annotations

from typing import Any, Dict, Optional

from core.auth.cookie_runtime_engine import extract_cookies, inject_cookies
from core.auth.session_restoration_engine import restore_authenticated_session
from core.auth.token_runtime_engine import extract_auth_tokens
from core.network.network_capture_engine import attach_network_capture
from core.identity.browser_identity_orchestrator import build_browser_identity
from core.session.browser_session_snapshot_engine import (
    capture_browser_session,
)

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None

MAX_HTML_SIZE = 10_000_000
DEFAULT_TIMEOUT_MS = 30000


def launch_authenticated_browser(
    session: Optional[Dict[str, Any]] = None,
    identity_profile: Optional[Dict[str, Any]] = None,
    persistent_identity: bool = False,
) -> Dict[str, Any]:
    session = session or {
        "cookies": [],
        "headers": {},
        "auth_tokens": [],
        "bounded": True,
    }

    identity = identity_profile or build_browser_identity("default")

    if sync_playwright is None:
        return {
            "available": False,
            "reason": "playwright_missing",
            "session": session,
            "identity": identity,
            "bounded": True,
        }

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)

    screen = identity.get("screen", {})
    languages = identity.get("languages", ["en-US"])

    context = browser.new_context(
        user_agent=str(identity.get("user_agent", "")),
        viewport={
            "width": int(screen.get("width", 1280)),
            "height": int(screen.get("height", 720)),
        },
        locale=str(languages[0]) if languages else "en-US",
        timezone_id=str(identity.get("timezone", "UTC")),
    )
    page = context.new_page()

    restore_authenticated_context(context, page, session)

    return {
        "available": True,
        "playwright": playwright,
        "browser": browser,
        "context": context,
        "page": page,
        "session": session,
        "identity": identity,
        "persistent_identity": persistent_identity,
        "bounded": True,
    }


def restore_authenticated_context(
    context: Any,
    page: Any,
    session: Dict[str, Any],
) -> Dict[str, Any]:
    headers = dict(session.get("headers", {}))

    if hasattr(page, "set_extra_http_headers") and headers:
        page.set_extra_http_headers(
            {str(k): str(v) for k, v in sorted(headers.items())}
        )

    return restore_authenticated_session(context, page, session)


def persist_authenticated_context(
    context: Any,
    page: Any,
    session: Dict[str, Any],
) -> Dict[str, Any]:
    snapshot = capture_browser_session(page, context)
    cookies = extract_cookies(context)
    tokens = extract_auth_tokens(page)

    merged = {
        **session,
        "cookies": cookies.get("cookies", []),
        "auth_tokens": tokens.get("tokens", []),
        "local_storage": snapshot.get("local_storage", {}),
        "session_storage": snapshot.get("session_storage", {}),
        "origin": snapshot.get("origin", session.get("origin", "")),
        "authenticated": True,
        "bounded": True,
    }

    return merged


def render_page(
    url: str,
    session: Dict[str, Any] | None = None,
    authenticated: bool = False,
    identity_profile: Optional[Dict[str, Any]] = None,
    persistent_identity: bool = False,
    adaptive_runtime: bool = False,
    selector_healing: bool = False,
    modal_recovery: bool = False,
    pagination_recovery: bool = False,
) -> Dict[str, Any]:
    if sync_playwright is None:
        return {
            "available": False,
            "reason": "playwright_missing",
            "bounded": True,
        }

    session = session or {}

    try:
        identity = identity_profile or build_browser_identity("default")

        if authenticated or persistent_identity:
            launched = launch_authenticated_browser(
                session,
                identity_profile=identity,
                persistent_identity=persistent_identity,
            )

            if not launched.get("available"):
                return launched

            playwright = launched["playwright"]
            browser = launched["browser"]
            context = launched["context"]
            page = launched["page"]
        else:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=True)
            screen = identity.get("screen", {})
            languages = identity.get("languages", ["en-US"])
            context = browser.new_context(
                user_agent=str(identity.get("user_agent", "")),
                viewport={
                    "width": int(screen.get("width", 1280)),
                    "height": int(screen.get("height", 720)),
                },
                locale=str(languages[0]) if languages else "en-US",
                timezone_id=str(identity.get("timezone", "UTC")),
            )
            page = context.new_page()

            headers = session.get("headers", {})
            if isinstance(headers, dict) and headers:
                page.set_extra_http_headers(
                    {str(k): str(v) for k, v in sorted(headers.items())}
                )

        network = attach_network_capture(page)

        page.goto(
            url,
            wait_until="networkidle",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        html = page.content()
        title = page.title()

        updated_session = persist_authenticated_context(
            context,
            page,
            session,
        )

        browser.close()
        playwright.stop()

        return {
            "available": True,
            "url": url,
            "title": title,
            "html": html[:MAX_HTML_SIZE],
            "network": {
                "requests": sorted(
                    network.get("requests", []),
                    key=lambda item: (
                        str(item.get("url")),
                        str(item.get("method")),
                    ),
                ),
                "bounded": True,
            },
            "session": updated_session,
            "identity": identity,
            "authenticated": authenticated,
            "persistent_identity": persistent_identity,
            "adaptive_runtime": adaptive_runtime,
            "selector_healing": selector_healing,
            "modal_recovery": modal_recovery,
            "pagination_recovery": pagination_recovery,
            "bounded": True,
        }
    except Exception as exc:
        return {
            "available": False,
            "reason": str(exc)[:500],
            "url": url,
            "bounded": True,
        }
