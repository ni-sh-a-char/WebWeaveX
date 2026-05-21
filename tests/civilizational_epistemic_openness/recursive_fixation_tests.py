from core.evidence.semantic_fixation_engine import detect_semantic_fixation
from core.evidence.explanatory_fixation_engine import detect_explanatory_fixation
from core.evidence.ontology_fixation_engine import detect_ontology_fixation
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_semantic_fixation_suppressed():
    r = detect_semantic_fixation(key_uniformity=True, depth=3)
    assert r["fixation"] is True
    assert r["suppress"] is True


def test_explanatory_fixation_low_alternatives():
    r = detect_explanatory_fixation(alternative_count=0, depth=3)
    assert r["fixation"] is True


def test_bundle_fixation_flags():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert_openness_bundle(r)
    assert "semantic_fixation_suppressed" in r
