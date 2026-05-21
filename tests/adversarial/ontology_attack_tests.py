from core.knowledge.ontology_validation_engine import validate_ontology_edge


def test_attack_edge_rejected():
    r = validate_ontology_edge({"from": "a", "to": "b", "type": "evil"})
    assert r["valid"] is False
