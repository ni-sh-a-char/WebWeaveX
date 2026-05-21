from __future__ import annotations

from typing import Any, Dict, List


def terminate_stabilization(suppressed: List[Dict[str, Any]], unstable_regions: List[str]) -> Dict[str, Any]:
    terminated = [s.get("reason", "") for s in suppressed] + unstable_regions
    return {"terminated": sorted(set(t for t in terminated if t)), "chain_stopped": bool(terminated)}
