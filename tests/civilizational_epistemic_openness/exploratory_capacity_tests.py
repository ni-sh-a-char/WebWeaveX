from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_exploratory_capacity_with_ambiguity():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1}, ambiguities=["unknown"])
    assert_openness_bundle(r)
    assert r["exploratory_capacity"]["preserved"] is True
    assert r["exploratory_capacity"]["capacity"] is True


def test_semantic_exploration_active():
    r = structure_cognition({"a": 1, "b": 2}, {"c": 3}, {"a": 1})
    assert r["semantic_exploration"]["active"] is True
