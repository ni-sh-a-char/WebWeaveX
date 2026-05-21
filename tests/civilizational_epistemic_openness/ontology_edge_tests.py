from core.knowledge.speculative_ontology_engine import suppress_speculative_ontology_edge


def test_speculative_ontology_openness():
    edge = suppress_speculative_ontology_edge({"from": "a", "to": "b", "evidence": ["e1"]})
    assert edge.get("civilizational_openness", {}).get("open") is True
    assert edge.get("ontology_exploration", {}).get("active") is True
