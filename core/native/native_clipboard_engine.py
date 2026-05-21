from __future__ import annotations

from typing import Any, Dict, Optional


def capture_native_clipboard(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}

    return {
        "text": str(snap.get("text", "")),
        "formats": list(snap.get("formats", [])),
        "available": bool(snap.get("text")),
        "bounded": True,
    }
