from core.knowledge.ontology_evolution_engine import evolve_ontology
from core.knowledge.ontology_diff_engine import diff_ontology_edges


def test_ontology_diff():
    d = diff_ontology_edges([{"from": "a", "to": "b"}], [{"from": "a", "to": "b"}, {"from": "c", "to": "d"}])
    assert d["added"] == 1


def test_ontology_evolve():
    e = evolve_ontology([], [{"from": "x", "to": "y", "evidence": ["e"]}])
    assert e["evolved"] is True
