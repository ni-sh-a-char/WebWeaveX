from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_propagation(seed: str, edges: List[Dict[str, Any]], max_hops: int = 5) -> Dict[str, Any]:
    visited = {seed}
    frontier = [seed]
    hops = 0
    while frontier and hops < max_hops:
        next_f = []
        for e in edges:
            if e.get("from") in frontier and e.get("to") not in visited:
                visited.add(str(e["to"]))
                next_f.append(str(e["to"]))
        frontier = next_f
        hops += 1
    return {"visited": sorted(visited), "hops": hops, "bounded": hops <= max_hops}
