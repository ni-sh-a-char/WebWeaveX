from __future__ import annotations

from typing import Any, Dict


def model_semantic_self_determination(independent: bool, depth: int) -> Dict[str, Any]:
    return {
        "self_determined": independent,
        "dependency_blocked": True,
        "obedience_blocked": True,
        "depth": depth,
    }
