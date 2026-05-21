from __future__ import annotations

from typing import Any, Dict


def account_semantic_resources(
    state: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "memory_objects": len(state),
        "resource_bounded": True,
    }
