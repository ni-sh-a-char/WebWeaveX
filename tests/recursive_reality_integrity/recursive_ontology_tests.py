from core.knowledge.ontology_engine import build_ontology


def test_ontology():
    assert build_ontology(["X"], [])["reconciled"]["entities"]
