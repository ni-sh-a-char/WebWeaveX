from __future__ import annotations

from typing import Any, Dict, List, Optional


_SCOPES = ("browser", "native", "filesystem", "connector", "terminal", "vm")


def build_runtime_permissions(
    scopes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    active = sorted(set(scopes or ["browser", "native"]))
    return {
        "scopes": {scope: scope in active for scope in _SCOPES},
        "active_scopes": active,
        "bounded": True,
    }


def validate_runtime_permissions(
    permissions: Dict[str, Any],
    runtime: str,
    action_type: str,
) -> Dict[str, Any]:
    scopes = permissions.get("scopes", {})
    runtime_scope = runtime if runtime in _SCOPES else "browser"

    if action_type.startswith("terminal_") or action_type == "terminal_command":
        runtime_scope = "terminal"
    elif action_type.startswith("native_"):
        runtime_scope = "native"
    elif action_type.startswith("vm_"):
        runtime_scope = "vm"
    elif action_type.startswith("connector_"):
        runtime_scope = "connector"

    allowed = bool(scopes.get(runtime_scope, False))
    return {
        "allowed": allowed,
        "scope": runtime_scope,
        "deterministic": True,
        "bounded": True,
    }
