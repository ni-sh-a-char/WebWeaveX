from __future__ import annotations

from core.documents.concept_progression_engine import model_concept_progression


def model_conceptual_transitions(text: str):
    return model_concept_progression(text)
