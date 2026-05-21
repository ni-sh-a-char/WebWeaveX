from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_transition_engine import model_semantic_transitions


def model_concept_progression(text: str) -> Dict[str, Any]:
    trans = model_semantic_transitions(text)
    progression: List[Dict[str, Any]] = []
    for i, t in enumerate(trans.get("transitions", [])):
        progression.append({"index": i, "from": t.get("from"), "to": t.get("to"), "introduces": t.get("to")})
    return {
        "progression": progression,
        "concept_count": len(progression),
        "deterministic_inputs": [f"concepts={len(progression)}"],
    }
