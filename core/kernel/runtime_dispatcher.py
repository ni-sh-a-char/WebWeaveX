from __future__ import annotations

from typing import Any, Callable, Dict, Optional


def dispatch_runtime_phase(
    phase: str,
    handler: Callable[..., Dict[str, Any]],
    context: Dict[str, Any],
    **kwargs: Any,
) -> Dict[str, Any]:
    result = handler(context=context, **kwargs)
    return {
        "phase": phase,
        "result": result,
        "dispatched": True,
        "bounded": True,
    }
