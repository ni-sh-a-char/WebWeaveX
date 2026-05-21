from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_policy(
    allow_terminal: bool = False,
    allow_browser_mutation: bool = True,
    max_mutations: int = 100,
    max_actions: int = 1000,
    max_depth: int = 50,
    require_rollback: bool = True,
    replay_guaranteed: bool = True,
) -> Dict[str, Any]:
    return {
        "allow_terminal": allow_terminal,
        "allow_browser_mutation": allow_browser_mutation,
        "max_mutations": max_mutations,
        "max_actions": max_actions,
        "max_depth": max_depth,
        "forbidden_actions": [] if allow_terminal else ["terminal_command"],
        "rollback_required": require_rollback,
        "replay_guaranteed": replay_guaranteed,
        "bounded": True,
    }


def enforce_runtime_policy(
    policy: Dict[str, Any],
    action: Dict[str, Any],
    mutation_count: int = 0,
    action_count: int = 0,
) -> Dict[str, Any]:
    action_type = str(action.get("action_type", action.get("type", "")))
    forbidden = set(policy.get("forbidden_actions", []))

    allowed = action_type not in forbidden
    if action_type == "terminal_command" and not policy.get("allow_terminal", False):
        allowed = False
    if action_type.startswith("browser_") and not policy.get("allow_browser_mutation", True):
        allowed = False

    within_mutations = mutation_count <= int(policy.get("max_mutations", 100))
    within_actions = action_count <= int(policy.get("max_actions", 1000))

    return {
        "allowed": allowed and within_mutations and within_actions,
        "within_bounds": within_mutations and within_actions,
        "policy_violation": not allowed,
        "bounded": True,
    }
