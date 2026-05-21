from __future__ import annotations

from typing import Any, Dict, List


def terminate_recursive_stabilization(suppressed: List[Dict[str, Any]], depth: int) -> Dict[str, Any]:
    terminated = [s.get("reason", "") for s in suppressed] + ([f"depth_{depth}_limit"] if depth >= 4 else [])
    return {"terminated": sorted(set(t for t in terminated if t)), "chain_stopped": bool(terminated)}
