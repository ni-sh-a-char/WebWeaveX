from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_websocket_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "protocol": "websocket",
        "connections": list(snap.get("connections", [])),
        "frames": int(snap.get("frames", 0)),
        "bounded": True,
    }
