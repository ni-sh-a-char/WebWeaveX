from __future__ import annotations

from typing import Any, Dict


def assess_runtime_health(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "healthy": bool(runtime),
        "runtime_size": len(runtime),
    }
