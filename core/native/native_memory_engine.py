from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def save_native_runtime(
    path: str,
    runtime: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    encrypted = encrypt_session_state(runtime, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(encrypted, sort_keys=True), encoding="utf-8")
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_native_runtime(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "runtime": _empty_runtime(), "bounded": True}
    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)
    return {
        "available": True,
        "runtime": decrypted.get("session", _empty_runtime()),
        "algorithm": "kaalka",
        "bounded": True,
    }


def remember_native_runtime(
    memory: Dict[str, Any],
    update: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(memory)
    for key in (
        "accessibility_trees",
        "windows",
        "workflows",
        "runtime_graphs",
        "electron_state",
        "terminal_streams",
    ):
        merged.setdefault(key, update.get(key, merged.get(key, {})))
    merged.update(update)
    merged["bounded"] = True
    return merged


def _empty_runtime() -> Dict[str, Any]:
    return {
        "accessibility_trees": {},
        "windows": {},
        "workflows": {},
        "runtime_graphs": {},
        "electron_state": {},
        "terminal_streams": {},
        "bounded": True,
    }
