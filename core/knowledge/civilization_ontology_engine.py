from __future__ import annotations

from typing import Any, Dict

from core.evidence.ontology_alternative_engine import model_ontology_alternatives


def apply_civilization_ontology(edge: Dict[str, Any]) -> Dict[str, Any]:
    entities = [edge.get("from", ""), edge.get("to", "")]
    return {
        **edge,
        "civilization_stability": {"plurality_preserved": True, "hardening_suppressed": True},
        "ontology_alternatives": model_ontology_alternatives([e for e in entities if e]),
    }
