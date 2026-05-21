from core.knowledge.ontology_engine import build_ontology


def test_ontology_truth_preservation():
    edge = build_ontology(["A"], [{"from": "A", "to": "B", "inferred": True}])["reconciled"]["relations"][0]
    assert "truth_preservation" in edge
    assert edge["truth_preservation"].get("self_confirmation_blocked") is True
