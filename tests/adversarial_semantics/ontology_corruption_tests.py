from core.knowledge.ontology_validation_engine import validate_ontology_edge


def test_corrupt_edge():
    assert validate_ontology_edge({"from": "a", "to": "b"})["valid"] is False
