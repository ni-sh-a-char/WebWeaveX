from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_electron_storage(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    indexed_db = sorted(
        snap.get("indexed_db", []),
        key=lambda item: str(item.get("name", "")),
    )
    local_storage = dict(sorted((snap.get("local_storage") or {}).items()))
    session_storage = dict(sorted((snap.get("session_storage") or {}).items()))
    return {
        "indexed_db": indexed_db,
        "local_storage": local_storage,
        "session_storage": session_storage,
        "bounded": True,
    }
