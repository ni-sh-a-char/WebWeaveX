from core.evidence.explanatory_divergence_engine import model_explanatory_divergence
from core.evidence.civilizational_epistemic_openness_engine import apply_civilizational_epistemic_openness
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_explanatory_divergence_alternatives():
    r = model_explanatory_divergence([{"id": "e1"}, {"id": "e2"}])
    assert r["preserved"] is True


def test_bundle_explanatory_divergence():
    bundle = {
        "observed": {"a": 1},
        "inferred": {"b": 2},
        "reconciled": {"a": 1},
        "explanatory_diversity": {"alternatives": [{"id": "x"}, {"id": "y"}]},
        "lineage": {"stages": [{"stage": "a"}, {"stage": "b"}]},
        "evidence": ["e1"],
        "ambiguities": [],
        "confidence_basis": {"score": 0.5},
    }
    out = apply_civilizational_epistemic_openness(bundle)
    assert_openness_bundle(out)
    assert out["explanatory_divergence"]["preserved"] is True
