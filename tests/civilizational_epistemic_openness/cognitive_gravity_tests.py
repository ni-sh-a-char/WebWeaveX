from core.evidence.cognitive_gravity_engine import detect_cognitive_gravity_well
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_gravity_well_suppressed():
    r = detect_cognitive_gravity_well(high_confidence=True, low_diversity=True, depth=3)
    assert r["gravity_well"] is True
    assert r["suppress"] is True


def test_bundle_gravity_suppression():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    r["confidence_basis"] = {"score": 0.9}
    from core.evidence.civilizational_epistemic_openness_engine import apply_civilizational_epistemic_openness

    out = apply_civilizational_epistemic_openness(r)
    assert_openness_bundle(out)
    assert "antigravity" in out
