from __future__ import annotations

from typing import Any, Dict, List


def terminate_semantic_chain(unstable_regions: List[str], continuity_refusals: List[Dict[str, Any]]) -> Dict[str, Any]:
    terminated = list(unstable_regions) + [r.get("target", "") for r in continuity_refusals]
    return {"terminated": sorted(set(t for t in terminated if t)), "chain_stopped": bool(terminated)}
