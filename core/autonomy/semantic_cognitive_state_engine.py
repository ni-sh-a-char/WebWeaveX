from __future__ import annotations

from typing import Any, Dict


def build_semantic_cognitive_state(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "state_keys": sorted(
            runtime.keys()
        ),
        "cognitive_depth": len(
            runtime
        ),
    }
