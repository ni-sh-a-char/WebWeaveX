from __future__ import annotations

from typing import Any, Dict


MAX_RUNTIME_SIZE = 100000


def enforce_semantic_safety_envelope(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "safe": (
            len(runtime)
            <= MAX_RUNTIME_SIZE
        ),
        "runtime_size": len(runtime),
    }
