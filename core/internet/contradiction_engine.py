from __future__ import annotations

from core.evidence.contradiction_evidence_engine import detect_contradiction_evidence


def detect_contradictions(snippets: list[str]):
    result = detect_contradiction_evidence(snippets)
    return {
        "contradiction_pairs": result.get("contradiction_pairs", []),
        "conflicts": result.get("conflicts", []),
        "evidence": result.get("evidence", []),
        "sources": result.get("sources", []),
        "grounding": result.get("grounding", {}),
        "lineage": result.get("lineage", {}),
        "confidence_basis": result.get("confidence_basis", {}),
    }
