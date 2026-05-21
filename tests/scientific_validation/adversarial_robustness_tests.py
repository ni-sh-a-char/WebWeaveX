from core.knowledge.ontology_consistency_engine import check_ontology_consistency


def test_corrupted_ontology_detected():
    r = check_ontology_consistency([{"from": "a", "to": "b", "type": "evil", "evidence": ["e"]}])
    assert r["consistent"] is False
