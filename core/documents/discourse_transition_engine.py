from __future__ import annotations

from core.documents.semantic_transition_engine import model_semantic_transitions

def model_discourse_transitions(text: str):
    return model_semantic_transitions(text)
