from __future__ import annotations

from typing import Any, Dict

from core.kernel.runtime_context import build_runtime_context
from core.kernel.runtime_policy import build_kernel_policy
from core.kernel.runtime_state import build_kernel_state


def initialize_runtime(
    runtime_type: str = "browser",
    tick: int = 0,
) -> Dict[str, Any]:
    context = build_runtime_context(runtime_type=runtime_type, tick=tick)
    policy = build_kernel_policy()
    state = build_kernel_state(context)
    return {
        "context": context,
        "policy": policy,
        "state": state,
        "initialized": True,
        "bounded": True,
    }


def shutdown_runtime(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "shutdown": True,
        "final_tick": int(state.get("tick", 0)),
        "bounded": True,
    }
