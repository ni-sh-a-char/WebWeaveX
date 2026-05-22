from __future__ import annotations

import sys
from typing import Any, Dict, List


def probe_windows_uia() -> Dict[str, Any]:
    """Optional Windows UIA binding with graceful degradation."""
    if sys.platform != "win32":
        return {"available": False, "reason": "not_windows", "bounded": True}
    try:
        import comtypes  # noqa: F401
        import comtypes.client  # noqa: F401

        return {
            "available": True,
            "backend": "uia",
            "windows": [],
            "nodes": [],
            "bounded": True,
        }
    except Exception as exc:
        return {
            "available": False,
            "reason": f"uia_unavailable:{type(exc).__name__}",
            "backend": "structural_fallback",
            "bounded": True,
        }


def extract_windows_uia_snapshot(fixture: Dict[str, Any]) -> Dict[str, Any]:
    probe = probe_windows_uia()
    if probe.get("available"):
        return {**probe, "fixture": fixture, "bounded": True}
    return {
        **probe,
        "windows": fixture.get("windows", []),
        "nodes": fixture.get("nodes", []),
        "bounded": True,
    }
