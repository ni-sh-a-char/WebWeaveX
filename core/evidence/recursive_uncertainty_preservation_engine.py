from __future__ import annotations

from typing import Any, Dict, List


def preserve_recursive_uncertainty(uncertainties: List[str], depth: int) -> Dict[str, Any]:
    return {
        "preserved": True,
        "items": sorted(set(str(u) for u in uncertainties)),
        "depth": depth,
        "collapse_suppressed": True,
    }
