from core.evidence import structure_cognition
from core.evidence.interpretive_divergence_engine import model_interpretive_divergence
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_interpretive_divergence_multiple():
    r = model_interpretive_divergence([{"id": "i1"}, {"id": "i2"}])
    assert r["exploration_maintained"] is True
    assert r["divergence"] > 1


def test_bundle_interpretive_exploration():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    r["interpretive_diversity"] = {"interpretations": [{"id": "x"}, {"id": "y"}]}
    from core.evidence.civilizational_epistemic_openness_engine import apply_civilizational_epistemic_openness

    out = apply_civilizational_epistemic_openness(r)
    assert out["interpretive_exploration"]["active"] is True
