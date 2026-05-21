from __future__ import annotations

from typing import Any, Dict, List

from core.documents.tutorial_causality_engine import reconstruct_tutorial_causality
from core.documents.discourse_transition_engine import model_discourse_transitions


def run_discourse_runtime(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    tutorial = reconstruct_tutorial_causality(sections)
    text = "\n".join(str(s.get("content", "")) for s in sections)
    transitions = model_discourse_transitions(text) if sections else {}
    return {
        "tutorial": tutorial,
        "transitions": transitions,
        "deterministic": True,
    }
