from core.internet.trust_uncertainty_engine import model_trust_uncertainty
from core.internet.semantic_reliability_engine import score_semantic_reliability


def test_trust_uncertainty_increases_with_contradiction():
    low = model_trust_uncertainty(5, 0, 2)
    high = model_trust_uncertainty(5, 3, 2)
    assert high["trust_uncertainty"] >= low["trust_uncertainty"]


def test_reliability_not_opaque():
    r = score_semantic_reliability(["parser:ast", "citation:1"], parser_backed=True)
    assert r["opaque"] is False
