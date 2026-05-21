from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def remember_application_runtime(
    memory: Dict[str, Any],
    update: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(memory)
    for key in (
        "workflows",
        "forms",
        "action_graphs",
        "navigation_flows",
        "dashboard_structures",
    ):
        merged.setdefault(key, update.get(key, merged.get(key, {})))
    merged.update(update)
    merged["bounded"] = True
    return merged


def restore_application_runtime(
    memory: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "memory": memory,
        "restored": bool(memory),
        "bounded": True,
    }


def save_application_memory(
    path: str,
    memory: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    encrypted = encrypt_session_state(memory, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(encrypted, sort_keys=True), encoding="utf-8")
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_application_memory(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "memory": _empty_memory(), "bounded": True}
    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)
    return {
        "available": True,
        "memory": decrypted.get("session", _empty_memory()),
        "algorithm": "kaalka",
        "bounded": True,
    }


def _empty_memory() -> Dict[str, Any]:
    return {
        "workflows": {},
        "forms": {},
        "action_graphs": {},
        "navigation_flows": {},
        "dashboard_structures": {},
        "bounded": True,
    }
