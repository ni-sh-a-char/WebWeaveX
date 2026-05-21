from __future__ import annotations

from core.evidence.contradiction_evidence_engine import detect_contradiction_evidence


def detect_contradictions(snippets: list[str]):
    return detect_contradiction_evidence(snippets)
