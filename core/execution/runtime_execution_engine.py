from __future__ import annotations

from typing import Any, Dict, Optional

from core.execution.runtime_action_engine import build_runtime_action
from core.execution.runtime_permissions_engine import validate_runtime_permissions
from core.execution.runtime_policy_engine import enforce_runtime_policy
from core.execution.runtime_sandbox_engine import build_runtime_sandbox

_SAFE_TERMINAL = frozenset({"pwd", "echo", "whoami"})
_FORBIDDEN_SHELL = frozenset({"rm", "del", "format", "shutdown", "eval", "exec"})


def _normalize_action(raw: Dict[str, Any], tick: int) -> Dict[str, Any]:
    action_type = str(raw.get("type", raw.get("action_type", "")))
    runtime = str(raw.get("runtime", "browser"))

    if action_type == "browser_click":
        runtime = "browser"
        payload = {"selector": str(raw.get("selector", ""))}
    elif action_type == "terminal_command":
        runtime = "terminal"
        payload = {"command": str(raw.get("command", ""))}
    elif action_type == "native_focus":
        runtime = "native"
        payload = {"window": str(raw.get("window", ""))}
    else:
        payload = dict(raw.get("payload", raw))

    return build_runtime_action(action_type, runtime, payload, tick=tick)


def _action_allowed_in_sandbox(sandbox: Dict[str, Any], action: Dict[str, Any]) -> bool:
    allowed = set(sandbox.get("allowed_actions", []))
    return action.get("action_type", "") in allowed


def _validate_terminal(command: str) -> bool:
    cmd = command.strip().split()[0] if command.strip() else ""
    if cmd in _FORBIDDEN_SHELL:
        return False
    return cmd in _SAFE_TERMINAL


def execute_runtime_action(
    raw_action: Dict[str, Any],
    sandbox: Optional[Dict[str, Any]] = None,
    policy: Optional[Dict[str, Any]] = None,
    permissions: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    mutation_count: int = 0,
    action_count: int = 0,
) -> Dict[str, Any]:
    sandbox = sandbox or build_runtime_sandbox()
    policy = policy or {}
    permissions = permissions or {}

    action = _normalize_action(raw_action, tick)
    runtime = action["runtime"]
    action_type = action["action_type"]

    if not _action_allowed_in_sandbox(sandbox, action):
        return {
            "executed": False,
            "action_id": action["id"],
            "runtime": runtime,
            "reason": "sandbox_forbidden",
            "bounded": True,
        }

    perm = validate_runtime_permissions(permissions, runtime, action_type)
    if not perm.get("allowed", False) and permissions:
        return {
            "executed": False,
            "action_id": action["id"],
            "runtime": runtime,
            "reason": "permission_denied",
            "bounded": True,
        }

    enforcement = enforce_runtime_policy(policy, action, mutation_count, action_count)
    if not enforcement.get("allowed", True):
        return {
            "executed": False,
            "action_id": action["id"],
            "runtime": runtime,
            "reason": "policy_violation",
            "bounded": True,
        }

    if action_type == "terminal_command":
        command = str(action.get("payload", {}).get("command", ""))
        if not _validate_terminal(command):
            return {
                "executed": False,
                "action_id": action["id"],
                "runtime": runtime,
                "reason": "unsafe_terminal",
                "bounded": True,
            }

    if action_type == "browser_click" and not action.get("payload", {}).get("selector"):
        return {
            "executed": False,
            "action_id": action["id"],
            "runtime": runtime,
            "reason": "invalid_selector",
            "bounded": True,
        }

    return {
        "executed": True,
        "action_id": action["id"],
        "runtime": runtime,
        "action": action,
        "bounded": True,
    }
