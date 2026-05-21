from __future__ import annotations

from typing import Any, Dict, Optional


def extract_ide_runtime(
    ide: str = "vscode",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "ide": ide,
        "open_files": sorted(snap.get("open_files", []), key=str),
        "terminals": list(snap.get("terminals", [])),
        "tabs": list(snap.get("tabs", [])),
        "workspace_topology": dict(snap.get("workspace", {})),
        "debug_sessions": list(snap.get("debug_sessions", [])),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
