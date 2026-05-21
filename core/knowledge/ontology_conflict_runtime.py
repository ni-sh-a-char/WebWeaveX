from __future__ import annotations

from core.knowledge.ontology_conflict_engine import detect_ontology_conflicts


def runtime_ontology_conflicts(edges):
    return detect_ontology_conflicts(edges)
