from core.knowledge.ontology_consistency_engine import check_ontology_consistency
from core.knowledge.semantic_merge_rigor_engine import merge_with_evidence


def test_missing_evidence_violation():
    r = check_ontology_consistency([{"from": "a", "to": "b"}])
    assert r["consistent"] is False


def test_silent_merge_forbidden():
    r = merge_with_evidence([{"evidence": []}])
    assert r["merged"] is False
