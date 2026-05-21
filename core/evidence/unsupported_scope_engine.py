from __future__ import annotations

from typing import Any, Dict, List


def model_unsupported_scope(dimensions: List[str]) -> Dict[str, Any]:
    dims = sorted(set(str(d) for d in (dimensions or []) if d))
    return {
        "dimensions": dims,
        "scope_unsupported": bool(dims),
        "count": len(dims),
    }
