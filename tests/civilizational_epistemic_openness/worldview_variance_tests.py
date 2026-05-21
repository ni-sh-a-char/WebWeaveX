from core.evidence import structure_cognition
from core.evidence.worldview_variance_engine import model_worldview_variance
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_worldview_variance_with_contradictions():
    r = model_worldview_variance(interpretation_count=3, contradiction_pairs=2)
    assert r["preserved"] is True
    assert r["variance"] > 0


def test_bundle_worldview_exploration():
    r = structure_cognition(
        {"a": 1},
        {"b": 2},
        {"a": 1},
        contradicted={"pairs": [["a", "b"]]},
    )
    assert_openness_bundle(r)
    assert r["worldview_variance"]["preserved"] is True
