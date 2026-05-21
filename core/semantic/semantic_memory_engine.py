from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value


def save_semantic_memory(
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


def load_semantic_memory(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "memory": _empty_memory(), "bounded": True}

    wrapper = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_value(wrapper["encrypted"], key)
    memory = json.loads(decrypted["decrypted"])

    return {
        "available": True,
        "memory": memory,
        "algorithm": "kaalka",
        "bounded": True,
    }


def remember_semantic_runtime(
    memory: Dict[str, Any],
    update: Dict[str, Any],
) -> Dict[str, Any]:
    merged = dict(memory)
    for field in (
        "ontology",
        "semantic_graph",
        "entity_mappings",
        "semantic_workflows",
        "runtime_semantics",
    ):
        merged.setdefault(field, update.get(field, merged.get(field, {})))
    merged.update(update)
    merged["bounded"] = True
    return merged


def _empty_memory() -> Dict[str, Any]:
    return {
        "ontology": {},
        "semantic_graph": {},
        "entity_mappings": {},
        "semantic_workflows": {},
        "runtime_semantics": {},
        "bounded": True,
    }
