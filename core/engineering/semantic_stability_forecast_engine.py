from __future__ import annotations

from typing import Any, Dict


MAX_STABLE_SIZE = 10000


def forecast_semantic_stability(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    size = len(runtime_ir)
    return {
        "stable": size < MAX_STABLE_SIZE,
        "runtime_size": size,
    }
