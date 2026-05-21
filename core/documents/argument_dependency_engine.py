from __future__ import annotations

from typing import Any, Dict, List


MAX_EDGES = 300


def build_argument_dependencies(text: str) -> Dict[str, Any]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    claims = [{"id": f"c{i}", "order": i, "content": ln} for i, ln in enumerate(lines)]
    r = reconstruct_argument_dependencies(claims)
    nodes = [{"id": c["id"], "content": c.get("content")} for c in claims]
    return {
        "dependencies": r.get("edges", []),
        "nodes": nodes,
        "evidence": ["discourse:argument_order"],
        "deterministic": True,
    }


def reconstruct_argument_dependencies(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(claims, key=lambda c: int(c.get("order", 0)))
    edges = []
    for idx in range(1, len(ordered)):
        prev_c, cur_c = ordered[idx - 1], ordered[idx]
        if cur_c.get("depends_on"):
            edges.append(
                {
                    "from": cur_c.get("depends_on"),
                    "to": cur_c.get("id"),
                    "metadata": {"kind": "argument_support", "basis": "explicit_dependency"},
                }
            )
        else:
            edges.append(
                {
                    "from": prev_c.get("id"),
                    "to": cur_c.get("id"),
                    "metadata": {"kind": "argument_sequence", "basis": "document_order"},
                }
            )
    return {"edges": edges[:MAX_EDGES], "count": min(len(edges), MAX_EDGES), "deterministic": True}
