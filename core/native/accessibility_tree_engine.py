from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional


ROLE_MAP = {
    "button": "buttons",
    "textbox": "text_inputs",
    "edit": "text_inputs",
    "label": "labels",
    "menu": "menus",
    "menubar": "menus",
    "list": "lists",
    "tab": "tabs",
    "dialog": "dialogs",
}


def extract_accessibility_tree(
    snapshot: Optional[Dict[str, Any]] = None,
    backend: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Structural accessibility tree extraction.

    Backends: Windows UIA, macOS AX, Linux AT-SPI (graceful degradation).
    """
    resolved_backend = backend or _resolve_backend()

    if snapshot is not None:
        return _compile_tree(snapshot, resolved_backend)

    try:
        return _extract_live_tree(resolved_backend)
    except Exception:
        return _empty_tree(resolved_backend, degraded=True)


def _resolve_backend() -> str:
    if sys.platform == "win32":
        return "uia"
    if sys.platform == "darwin":
        return "ax"
    return "at-spi"


def _compile_tree(
    snapshot: Dict[str, Any],
    backend: str,
) -> Dict[str, Any]:
    nodes = list(snapshot.get("nodes", snapshot.get("elements", [])))[:20000]
    buckets: Dict[str, List[Dict[str, Any]]] = {
        "buttons": [],
        "text_inputs": [],
        "labels": [],
        "menus": [],
        "lists": [],
        "tabs": [],
        "dialogs": [],
    }

    for node in nodes:
        role = str(node.get("role", "")).lower()
        bucket = ROLE_MAP.get(role)
        if bucket:
            buckets[bucket].append({
                "name": str(node.get("name", "")),
                "id": str(node.get("id", "")),
                "bounds": node.get("bounds", {}),
                "enabled": bool(node.get("enabled", True)),
            })

    return {
        **buckets,
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "backend": backend,
        "bounded": True,
    }


def _extract_live_tree(backend: str) -> Dict[str, Any]:
    return _empty_tree(backend, degraded=True, reason="live_binding_unavailable")


def _empty_tree(
    backend: str,
    degraded: bool = False,
    reason: str = "",
) -> Dict[str, Any]:
    return {
        "buttons": [],
        "text_inputs": [],
        "labels": [],
        "menus": [],
        "lists": [],
        "tabs": [],
        "dialogs": [],
        "nodes": [],
        "backend": backend,
        "degraded": degraded,
        "reason": reason,
        "bounded": True,
    }
