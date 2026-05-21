from __future__ import annotations

from typing import Any, Dict, List


def distribute_recursive_semantics(keys: List[str]) -> Dict[str, Any]:
    return {"distributed": len(set(keys)) > 1, "key_count": len(set(keys))}
