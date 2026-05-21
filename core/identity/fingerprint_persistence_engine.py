from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def save_browser_identity(
    path: str,
    identity: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    encrypted = encrypt_session_state(identity, key)

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(encrypted, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "saved": True,
        "path": str(target),
        "algorithm": "kaalka",
        "bounded": True,
    }


def load_browser_identity(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)

    if not target.exists():
        from core.identity.browser_identity_orchestrator import (
            build_browser_identity,
        )

        return {
            "available": False,
            "identity": build_browser_identity("default"),
            "bounded": True,
        }

    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)

    return {
        "available": True,
        "identity": decrypted.get("session", {}),
        "algorithm": "kaalka",
        "bounded": True,
    }
