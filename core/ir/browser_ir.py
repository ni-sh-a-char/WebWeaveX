from __future__ import annotations

import json
from typing import Any, Dict, Optional

from core.auth.csrf_runtime_engine import extract_csrf_tokens
from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload


def _session_fingerprint(session: Optional[Dict[str, Any]]) -> str:
    payload = session or {
        "cookies": [],
        "headers": {},
        "auth_tokens": [],
    }

    return compute_kaalka_hash_payload({
        "cookies": payload.get("cookies", []),
        "headers": payload.get("headers", {}),
        "auth_tokens": payload.get("auth_tokens", []),
        "local_storage": payload.get("local_storage", {}),
        "session_storage": payload.get("session_storage", {}),
    })


def compile_browser_ir(
    runtime: Dict[str, Any],
    dom: Dict[str, Any],
    extraction: Dict[str, Any],
    network: Dict[str, Any],
    session: Optional[Dict[str, Any]] = None,
    authenticated: bool = False,
    page: Any = None,
) -> Dict[str, Any]:
    session = session or runtime.get("session", {})
    csrf = extract_csrf_tokens(page) if page is not None else {"tokens": []}

    cookie_count = len(session.get("cookies", []))
    token_count = len(session.get("auth_tokens", []))
    csrf_detected = len(csrf.get("tokens", [])) > 0

    runtime_identity = compute_kaalka_hash_payload({
        "url": runtime.get("url", ""),
        "title": runtime.get("title", ""),
        "authenticated": authenticated,
    })

    return {
        "ir": "browser",
        "runtime": runtime,
        "dom": dom,
        "extraction": extraction,
        "network": network,
        "authenticated": authenticated,
        "session_fingerprint": _session_fingerprint(session),
        "cookie_count": cookie_count,
        "token_count": token_count,
        "csrf_detected": csrf_detected,
        "runtime_identity": runtime_identity,
        "bounded": True,
    }
