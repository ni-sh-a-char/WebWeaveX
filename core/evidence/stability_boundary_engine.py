from __future__ import annotations

from typing import Any, Dict, List


def model_stability_boundary(unstable_regions: List[str]) -> Dict[str, Any]:
    return {
        "broken": bool(unstable_regions),
        "regions": unstable_regions,
        "suppress_stabilization": bool(unstable_regions),
    }
