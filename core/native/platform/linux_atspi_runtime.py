from __future__ import annotations

import sys
from typing import Any, Dict


def probe_linux_atspi() -> Dict[str, Any]:
    if sys.platform != "linux":
        return {"available": False, "reason": "not_linux", "bounded": True}
    try:
        import pyatspi  # noqa: F401

        return {"available": True, "backend": "at-spi", "bounded": True}
    except Exception as exc:
        return {
            "available": False,
            "reason": f"atspi_unavailable:{type(exc).__name__}",
            "backend": "structural_fallback",
            "bounded": True,
        }


def extract_linux_atspi_snapshot(fixture: Dict[str, Any]) -> Dict[str, Any]:
    probe = probe_linux_atspi()
    if probe.get("available"):
        return {**probe, "fixture": fixture, "bounded": True}
    return {
        **probe,
        "windows": fixture.get("windows", []),
        "nodes": fixture.get("nodes", []),
        "bounded": True,
    }
