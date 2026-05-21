from core.knowledge.ontology_engine import build_ontology


def test_anti_capture_on_edge():
    edge = build_ontology(["A", "B"], [{"from": "A", "to": "B"}])["reconciled"]["relations"][0]
    assert "anti_capture" in edge
