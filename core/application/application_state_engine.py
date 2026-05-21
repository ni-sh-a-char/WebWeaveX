from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_application_state(
    route: str,
    forms: Optional[List[Dict[str, Any]]] = None,
    modals: Optional[List[Dict[str, Any]]] = None,
    widgets: Optional[List[Dict[str, Any]]] = None,
    tabs: Optional[List[Dict[str, Any]]] = None,
    authenticated: bool = False,
    runtime_state: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "route": str(route)[:2000],
        "forms": list(forms or [])[:500],
        "modals": list(modals or [])[:200],
        "widgets": list(widgets or [])[:1000],
        "tabs": list(tabs or [])[:100],
        "authenticated": bool(authenticated),
        "runtime_state": dict(runtime_state or {}),
        "bounded": True,
    }
