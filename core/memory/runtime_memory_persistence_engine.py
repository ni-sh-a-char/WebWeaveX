from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value


def save_runtime_memory(
    path: str,
    memory: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    payload = json.dumps(memory, sort_keys=True)
    encrypted = encrypt_value(payload, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"encrypted": encrypted["encrypted"], "algorithm": "kaalka"}, sort_keys=True),
        encoding="utf-8",
    )
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_runtime_memory(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "memory": _empty_store(), "bounded": True}

    wrapper = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_value(wrapper["encrypted"], key)
    memory = json.loads(decrypted["decrypted"])

    return {
        "available": True,
        "memory": memory,
        "algorithm": "kaalka",
        "bounded": True,
    }


def _empty_store() -> Dict[str, Any]:
    return {
        "runtime": {},
        "knowledge": {},
        "semantic": {},
        "index": {},
        "graph": {},
        "lineage": {},
        "bounded": True,
    }
