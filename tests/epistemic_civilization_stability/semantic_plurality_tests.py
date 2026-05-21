from core.evidence import structure_cognition
from tests.epistemic_civilization_stability.civilization_helpers import assert_civilization_bundle


def test_plurality_bundle():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1}, ambiguities=["x"])
    assert_civilization_bundle(r)
    assert r["semantic_plurality"]["preserved"] is True
