from core.evidence.semantic_attractor_engine import detect_semantic_attractor
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_attractor_suppressed_when_detected():
    r = detect_semantic_attractor(depth=3, interpretation_count=1, evidence_count=1)
    assert r["attractor"] is True
    assert len(r["suppressed"]) == 1
    assert r["suppressed"][0]["exploration_pressure"]["maintain"] is True


def test_no_attractor_with_diversity():
    r = detect_semantic_attractor(depth=1, interpretation_count=3, evidence_count=5)
    assert r["attractor"] is False
    assert r["suppressed"] == []


def test_bundle_attractor_suppression():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert_openness_bundle(r)
    assert isinstance(r["semantic_attractors_suppressed"], list)
