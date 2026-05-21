from core.evidence.recursive_phase_space_engine import model_recursive_phase_space
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_phase_space_preserved():
    r = model_recursive_phase_space(key_count=5, ambiguity_count=2, depth=2)
    assert r["preserved"] is True


def test_bundle_phase_space():
    r = structure_cognition({"a": 1, "b": 2}, {"c": 3}, {"a": 1})
    assert_openness_bundle(r)
    assert r["recursive_phase_space"]["preserved"] is True
