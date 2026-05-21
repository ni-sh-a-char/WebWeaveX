from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_sandbox(
    runtime: str = "browser",
    allowed_actions: Optional[List[str]] = None,
    rollback_enabled: bool = True,
    max_actions: int = 1000,
    timeout_ticks: int = 10000,
    replay_policy: str = "strict",
) -> Dict[str, Any]:
    default_allowed = [
        "browser_click",
        "browser_focus",
        "native_focus",
    ]
    if runtime == "terminal":
        default_allowed = ["terminal_command"]
    elif runtime == "native":
        default_allowed = ["native_focus"]
    elif runtime == "vm":
        default_allowed = ["vm_execute"]

    return {
        "runtime": runtime,
        "allowed_actions": sorted(allowed_actions or default_allowed),
        "rollback_enabled": rollback_enabled,
        "max_actions": max_actions,
        "execution_boundaries": {
            "max_depth": 50,
            "max_mutations": 100,
            "timeout_ticks": timeout_ticks,
        },
        "mutation_limits": {"max_mutations": 100},
        "rollback_policy": {"enabled": rollback_enabled},
        "timeout_policy": {"ticks": timeout_ticks},
        "replay_policy": replay_policy,
        "bounded": True,
    }
