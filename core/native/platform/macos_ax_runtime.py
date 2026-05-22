from __future__ import annotations

import sys
from typing import Any, Dict


def probe_macos_ax() -> Dict[str, Any]:
    if sys.platform != "darwin":
        return {"available": False, "reason": "not_macos", "bounded": True}
    try:
        from ApplicationServices import AXUIElementCreateApplication  # noqa: F401

        return {"available": True, "backend": "axapi", "bounded": True}
    except Exception as exc:
        return {
            "available": False,
            "reason": f"axapi_unavailable:{type(exc).__name__}",
            "backend": "structural_fallback",
            "bounded": True,
        }


def extract_macos_ax_snapshot(fixture: Dict[str, Any]) -> Dict[str, Any]:
    probe = probe_macos_ax()
    if probe.get("available"):
        return {**probe, "fixture": fixture, "bounded": True}
    return {
        **probe,
        "windows": fixture.get("windows", []),
        "nodes": fixture.get("nodes", []),
        "bounded": True,
    }
