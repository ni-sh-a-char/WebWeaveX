from __future__ import annotations

from typing import Any, Dict, List


def model_recursive_semantic_independence(keys: List[str], depth: int) -> Dict[str, Any]:
    return {"independent": len(set(keys)) > 1 or depth < 2, "reliance_blocked": True}
