from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.semantic_fragility_engine import model_fragility


def assess_causality_fragility(edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence = []
    for e in edges or []:
        evidence.extend(e.get("evidence", []) if isinstance(e, dict) else [])
    return model_fragility(sorted(set(evidence)), [], 0, 0)
