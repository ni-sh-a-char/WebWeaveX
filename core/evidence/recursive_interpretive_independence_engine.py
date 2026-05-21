from __future__ import annotations

from typing import Any, Dict


def model_recursive_interpretive_independence(count: int) -> Dict[str, Any]:
    return {"independent": count > 1, "collapse_blocked": True}
