from core.evidence.recursive_stabilization_engine import detect_recursive_stabilization
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_stabilization_suppressed():
    r = detect_recursive_stabilization(reconciled_eq_inferred=True, depth=3)
    assert r["stabilized"] is True
    assert r["suppress"] is True


def test_bundle_stabilization_suppressed():
    r = structure_cognition({"a": 1}, {"a": 1}, {"a": 1})
    assert_openness_bundle(r)
    assert "recursive_stabilization_suppressed" in r
