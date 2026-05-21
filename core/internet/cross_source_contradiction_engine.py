from __future__ import annotations

from typing import Any, Dict, List

from core.internet.evidence_conflict_engine import detect_evidence_conflicts


def map_cross_source_contradictions(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    return detect_evidence_conflicts(claims)
