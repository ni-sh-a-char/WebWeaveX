from __future__ import annotations

from typing import Any, Dict, Optional


REMOTE_PROTOCOLS = ("rdp", "vnc", "ssh", "browser_remote")


def extract_remote_runtime(
    protocol: str = "ssh",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    normalized = protocol.lower()

    if normalized not in REMOTE_PROTOCOLS:
        normalized = "ssh"

    return {
        "protocol": normalized,
        "session_id": str(snap.get("session_id", "")),
        "host": str(snap.get("host", "")),
        "port": int(snap.get("port", 0)),
        "terminal": snap.get("terminal", {}),
        "window_stream": snap.get("window_stream", {}),
        "authenticated": bool(snap.get("authenticated", False)),
        "bounded": True,
    }
