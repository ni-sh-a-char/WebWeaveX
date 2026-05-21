from core.evidence import structure_cognition
from core.evidence.semantic_divergence_engine import model_semantic_divergence
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_semantic_divergence_engine_preserves_phase_space():
    r = model_semantic_divergence({"a": 1, "b": 2}, {"c": 3}, ["x"])
    assert r["preserved"] is True
    assert r["phase_space_maintained"] is True
    assert r["divergence_score"] > 0


def test_structure_cognition_semantic_divergence():
    r = structure_cognition({"a": 1, "b": 2}, {"c": 3}, {"a": 1})
    assert_openness_bundle(r)
    assert r["semantic_divergence"]["preserved"] is True
