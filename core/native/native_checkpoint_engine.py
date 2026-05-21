from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def save_native_checkpoint(
    path: str,
    checkpoint: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    encrypted = encrypt_session_state(checkpoint, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(encrypted, sort_keys=True), encoding="utf-8")
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_native_checkpoint(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "checkpoint": _empty_checkpoint(), "bounded": True}
    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)
    return {
        "available": True,
        "checkpoint": decrypted.get("session", _empty_checkpoint()),
        "algorithm": "kaalka",
        "bounded": True,
    }


def _empty_checkpoint() -> Dict[str, Any]:
    return {
        "runtime_state": {},
        "windows": {},
        "streams": {},
        "terminals": {},
        "workflows": {},
        "adaptive_state": {},
        "bounded": True,
    }
