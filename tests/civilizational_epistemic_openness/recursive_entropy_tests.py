from core.evidence.recursive_entropy_preservation_engine import preserve_recursive_entropy
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_entropy_preserved_with_ambiguity():
    r = preserve_recursive_entropy(ambiguities=["a"], uncertainties=["b"], depth=2)
    assert r["preserved"] is True


def test_bundle_entropy():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1}, ambiguities=["x"])
    assert_openness_bundle(r)
    assert r["recursive_entropy_preservation"]["preserved"] is True
