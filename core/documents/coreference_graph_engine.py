from __future__ import annotations

from typing import Any, Dict

from core.documents.coreference_resolution_engine import resolve_coreferences
from core.documents.rhetorical_parser_engine import parse_rhetorical_structure


def build_coreference_graph(text: str) -> Dict[str, Any]:
    coref = resolve_coreferences(text)
    rhet = parse_rhetorical_structure(text)
    headings = [u.get("title", "") for u in rhet.get("units", []) if u.get("type") == "heading"]
    nodes = [{"id": h, "kind": "entity"} for h in headings if h]
    edges = [
        {"from": c.get("pronoun", ""), "to": c.get("antecedent", ""), "evidence": ["discourse:coref"]}
        for c in coref.get("chains", [])
        if c.get("antecedent")
    ]
    return {"nodes": nodes, "edges": edges[:100], "chains": coref.get("chains", [])}
