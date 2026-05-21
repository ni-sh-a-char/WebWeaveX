from __future__ import annotations

from typing import Dict, List


def build_source_lineage(chain: List[str]) -> Dict[str, object]:
    ordered = [str(u) for u in (chain or []) if u]
    edges = [{"from": ordered[i], "to": ordered[i + 1]} for i in range(len(ordered) - 1)]
    return {"chain": ordered, "edges": edges, "depth": len(ordered)}
