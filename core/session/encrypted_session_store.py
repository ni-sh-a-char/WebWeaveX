from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def save_encrypted_session(
    path: str,
    session: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    payload = encrypt_session_state(session, key)

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text(
        json.dumps(payload, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "saved": True,
        "path": str(target),
        "algorithm": "kaalka",
        "bounded": True,
    }


def load_encrypted_session(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)

    if not target.exists():
        return {
            "available": False,
            "session": {
                "cookies": [],
                "headers": {},
                "auth_tokens": [],
                "local_storage": {},
                "session_storage": {},
                "authenticated": False,
                "bounded": True,
            },
            "bounded": True,
        }

    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "available": False,
            "reason": str(exc)[:200],
            "session": {
                "cookies": [],
                "headers": {},
                "auth_tokens": [],
                "bounded": True,
            },
            "bounded": True,
        }

    decrypted = decrypt_session_state(payload, key)

    return {
        "available": True,
        "session": decrypted.get("session", {}),
        "algorithm": "kaalka",
        "bounded": True,
    }
