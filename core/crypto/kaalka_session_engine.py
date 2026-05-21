from __future__ import annotations

import json
from typing import Any, Dict

from core.crypto.kaalka_runtime_engine import (
    decrypt_value,
    encrypt_value,
)

MAX_SESSION_BYTES = 10_000_000


def encrypt_session_state(
    session: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    serialized = json.dumps(
        session,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )[:MAX_SESSION_BYTES]

    encrypted = encrypt_value(serialized, key)

    return {
        **encrypted,
        "payload_type": "session",
        "bounded": True,
    }


def decrypt_session_state(
    payload: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    ciphertext = str(payload.get("encrypted", ""))

    decrypted = decrypt_value(ciphertext, key)
    text = str(decrypted.get("decrypted", ""))

    session = json.loads(text[:MAX_SESSION_BYTES])

    return {
        "session": session,
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }
