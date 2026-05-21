from core.knowledge.ontology_engine import build_ontology


def test_ontology_recursive_fields():
    edge = build_ontology(["A"], [{"from": "A", "to": "B"}])["reconciled"]["relations"][0]
    assert "recursive_reality_integrity" in edge
