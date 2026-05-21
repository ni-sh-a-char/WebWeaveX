from core.knowledge.ontology_engine import build_ontology


def test_ontology_civilization():
    edge = build_ontology(["A"], [{"from": "A", "to": "B"}])["reconciled"]["relations"][0]
    assert "civilization_stability" in edge
