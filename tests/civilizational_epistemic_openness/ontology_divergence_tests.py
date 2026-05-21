from core.evidence import structure_cognition
from core.evidence.ontology_divergence_engine import model_ontology_divergence
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_ontology_divergence_multiple_entities():
    r = model_ontology_divergence(["a", "b", "c"], depth=2)
    assert r["preserved"] is True
    assert r["divergence"] > 1


def test_bundle_ontology_exploration():
    r = structure_cognition({"x": 1}, {"y": 2, "z": 3}, {"x": 1})
    assert_openness_bundle(r)
    assert r["ontology_exploration"]["active"] is True
