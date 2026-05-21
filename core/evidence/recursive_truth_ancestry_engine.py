from __future__ import annotations

from typing import Any, Dict, List


def track_recursive_truth_ancestry(truth_refusals: List[Dict[str, Any]], depth: int) -> Dict[str, Any]:
    return {"refusals": truth_refusals, "depth": depth, "preserved": True}
