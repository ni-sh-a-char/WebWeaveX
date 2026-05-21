from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value


def save_memory_checkpoint(
    path: str,
    checkpoint: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    payload = json.dumps(checkpoint, sort_keys=True)
    encrypted = encrypt_value(payload, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"encrypted": encrypted["encrypted"], "algorithm": "kaalka"}, sort_keys=True),
        encoding="utf-8",
    )
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_memory_checkpoint(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "checkpoint": {}, "bounded": True}

    wrapper = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_value(wrapper["encrypted"], key)
    return {
        "available": True,
        "checkpoint": json.loads(decrypted["decrypted"]),
        "algorithm": "kaalka",
        "bounded": True,
    }
