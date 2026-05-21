from __future__ import annotations

from typing import Any, Dict


MAX_STABLE_RUNTIME = 10000


def analyze_semantic_stability(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    stable = len(runtime) < MAX_STABLE_RUNTIME

    return {
        "stable": stable,
        "runtime_size": len(runtime),
    }
