from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def save_interaction_replay(
    path: str,
    interactions: List[Dict[str, Any]],
    key: str,
) -> Dict[str, Any]:
    payload = {
        "interactions": list(interactions),
        "bounded": True,
    }

    encrypted = encrypt_session_state(payload, key)

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


def load_interaction_replay(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)

    if not target.exists():
        return {
            "available": False,
            "interactions": [],
            "bounded": True,
        }

    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)
    session_payload = decrypted.get("session", {})

    return {
        "available": True,
        "interactions": list(
            session_payload.get("interactions", [])
        ),
        "algorithm": "kaalka",
        "bounded": True,
    }
