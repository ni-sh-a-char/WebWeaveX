from __future__ import annotations

from typing import Any, Dict, List, Optional


def capture_native_streams(
    terminal: Optional[Dict[str, Any]] = None,
    desktop: Optional[Dict[str, Any]] = None,
    electron: Optional[Dict[str, Any]] = None,
    mutations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    terminal = terminal or {}
    desktop = desktop or {}
    electron = electron or {}
    mutations = list(mutations or [])

    return {
        "terminal_streams": [{
            "stream_id": terminal.get("stream_id", ""),
            "lines": len(terminal.get("output", [])),
        }] if terminal else [],
        "notifications": list(desktop.get("notifications", [])),
        "electron_updates": list(electron.get("routes", [])),
        "mutations": mutations[:10000],
        "bounded": True,
    }
