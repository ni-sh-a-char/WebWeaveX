from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_relationships(symbols: List[Any], dependencies: List[Any]) -> Dict[str, Any]:
    sym = sorted(set(str(s).strip().lower() for s in symbols or [] if s))
    deps = sorted(set(str(d).strip().lower() for d in dependencies or [] if d))
    edges = [{"from": sym[i], "to": sym[i + 1]} for i in range(max(0, len(sym) - 1))]
    for d in deps[:50]:
        if sym:
            edges.append({"from": sym[0], "to": d})
    return {"nodes": sym, "edges": sorted(edges, key=lambda e: (e["from"], e["to"]))}
