from core.knowledge.ontology_consistency_engine import check_ontology_consistency


def test_adversarial_type_field():
    r = check_ontology_consistency([{"from": "a", "to": "b", "type": "x", "evidence": ["e"]}])
    assert r["consistent"] is False
