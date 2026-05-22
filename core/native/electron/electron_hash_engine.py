from __future__ import annotations

import json
from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash


def stable_electron_runtime_hash(payload: Dict[str, Any]) -> str:
    """Deterministic Electron runtime fingerprint."""
    canonical = {
        "cdp": sorted(
            (payload.get("cdp") or {}).get("endpoints", []),
            key=lambda e: str(e.get("method", "")),
        ),
        "routes": sorted(
            (payload.get("routes") or {}).get("routes", []),
            key=lambda r: str(r.get("path", "")),
        ),
        "ipc": sorted(
            (payload.get("ipc") or {}).get("channels", []),
            key=lambda c: str(c.get("channel", "")),
        ),
        "storage": {
            "indexed_db": sorted(
                (payload.get("storage") or {}).get("indexed_db", []),
                key=lambda x: str(x),
            ),
            "local_storage": sorted(
                ((payload.get("storage") or {}).get("local_storage") or {}).items()
            ),
        },
    }
    return compute_kaalka_hash(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    )
