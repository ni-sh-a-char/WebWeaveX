from __future__ import annotations

from core.documents.instructional_semantics_engine import analyze_instructional_semantics


def extract_tutorial_flow(text: str):
    return analyze_instructional_semantics(text)
