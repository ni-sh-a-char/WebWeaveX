from core.evidence import structure_cognition, attach_epistemic_state
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_full_epistemic_stack_includes_openness():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert "epistemic_sovereignty" in r
    assert "cognitive_anti_capture" in r
    assert_openness_bundle(r)


def test_attach_epistemic_state_openness():
    base = {"observed": {}, "inferred": {"x": 1}, "reconciled": {}, "lineage": {"stages": []}, "evidence": [], "ambiguities": [], "confidence_basis": {"score": 0.5}}
    r = attach_epistemic_state(base)
    assert_openness_bundle(r)
