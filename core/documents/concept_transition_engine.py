from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_discourse_parser import parse_semantic_discourse


def model_concept_transitions(text: str) -> Dict[str, Any]:
    d = parse_semantic_discourse(text)
    transitions: List[Dict[str, str]] = []
    for e in d.get("transitions", []):
        if isinstance(e, dict) and e.get("from") and e.get("to"):
            transitions.append({"from": e["from"], "to": e["to"], "kind": "discourse"})
    return {"transitions": transitions, "count": len(transitions)}
