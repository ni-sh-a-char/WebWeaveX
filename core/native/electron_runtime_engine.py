from __future__ import annotations

from typing import Any, Dict, Optional


ELECTRON_APPS = {
    "discord": {"routes": ["/channels/@me"], "storage_keys": ["token", "user"]},
    "slack": {"routes": ["/client"], "storage_keys": ["team", "user"]},
    "vscode": {"routes": ["/workspace"], "storage_keys": ["workspace"]},
    "notion": {"routes": ["/"], "storage_keys": ["user"]},
    "figma": {"routes": ["/file"], "storage_keys": ["file"]},
}


def extract_electron_runtime(
    application: str = "",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    app_key = application.lower().strip()
    profile = ELECTRON_APPS.get(app_key, {"routes": ["/"], "storage_keys": []})
    snap = snapshot or {}

    return {
        "application": app_key or "electron",
        "chromium_runtime": {
            "version": str(snap.get("chromium_version", "structural")),
            "bounded": True,
        },
        "routes": sorted(
            list(snap.get("routes", profile.get("routes", []))),
            key=str,
        ),
        "internal_storage": dict(snap.get("internal_storage", {})),
        "indexed_db": list(snap.get("indexed_db", []))[:1000],
        "windows": list(snap.get("windows", [])),
        "preload_state": dict(snap.get("preload_state", {})),
        "bounded": True,
    }
