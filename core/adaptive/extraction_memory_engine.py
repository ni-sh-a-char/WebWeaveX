from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def remember_extraction_runtime(
    memory: Dict[str, Any],
    update: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(memory)
    merged.setdefault("selectors", {})
    merged.setdefault("healed_selectors", {})
    merged.setdefault("pagination_patterns", [])
    merged.setdefault("modal_solutions", [])
    merged.setdefault("interaction_chains", [])

    for key, value in update.items():
        merged[key] = value

    merged["bounded"] = True
    return merged


def restore_extraction_runtime(
    memory: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "memory": memory,
        "restored": bool(memory),
        "bounded": True,
    }


def save_adaptive_memory(
    path: str,
    memory: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    encrypted = encrypt_session_state(memory, key)

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


def load_adaptive_memory(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)

    if not target.exists():
        return {
            "available": False,
            "memory": _empty_memory(),
            "bounded": True,
        }

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
        "selectors": {},
        "healed_selectors": {},
        "pagination_patterns": [],
        "modal_solutions": [],
        "interaction_chains": [],
        "bounded": True,
    }
