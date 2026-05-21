from core.evidence import structure_cognition
from core.evidence.recursive_novelty_engine import model_recursive_novelty
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_recursive_novelty_preserved():
    r = model_recursive_novelty(depth=1, key_count=5, ambiguity_count=2)
    assert r["preserved"] is True
    assert r["exhaustion_blocked"] is True
    assert r["novelty"] > 0.1


def test_bundle_novelty_preservation():
    r = structure_cognition({"a": 1, "b": 2}, {"c": 3}, {"a": 1}, ambiguities=["ambig"])
    assert_openness_bundle(r)
    assert r["novelty_preservation"]["preserved"] is True
