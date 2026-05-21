from __future__ import annotations

from typing import Any, Dict, List

from core.documents.concept_transition_engine import model_concept_transitions
from core.documents.rhetorical_parser_engine import parse_rhetorical_structure


def model_semantic_transitions(text: str) -> Dict[str, Any]:
    trans = model_concept_transitions(text)
    rhet = parse_rhetorical_structure(text)
    headings = [u for u in rhet.get("units", []) if u.get("type") == "heading"]
    transitions: List[Dict[str, str]] = list(trans.get("transitions", []))
    for i in range(len(headings) - 1):
        transitions.append({
            "from": headings[i].get("title", ""),
            "to": headings[i + 1].get("title", ""),
            "kind": "section_transition",
        })
    return {"transitions": transitions, "count": len(transitions), "evidence": ["discourse:transitions"]}
