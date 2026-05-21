from __future__ import annotations

from typing import Any, Dict, List

from core.documents.rhetorical_structure_engine import extract_rhetorical_structure


def build_argument_graph(text: str) -> Dict[str, Any]:
    rhet = extract_rhetorical_structure(text)
    headings = [u for u in rhet["units"] if u.get("type") == "heading"]
    nodes = [{"id": f"h{i}", "role": "claim" if i == 0 else "support", "title": h.get("title", "")} for i, h in enumerate(headings)]
    edges = [{"from": nodes[i]["id"], "to": nodes[i + 1]["id"]} for i in range(len(nodes) - 1)]
    return {"nodes": nodes, "edges": edges, "deterministic_inputs": [f"nodes={len(nodes)}"]}
