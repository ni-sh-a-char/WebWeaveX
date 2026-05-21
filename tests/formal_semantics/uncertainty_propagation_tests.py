from core.evidence.uncertainty_propagation_math import propagate_uncertainty_math


def test_propagation_increases_with_ambiguity():
    low = propagate_uncertainty_math(3, 0, 0)
    high = propagate_uncertainty_math(3, 3, 1)
    assert high["uncertainty_score"] >= low["uncertainty_score"]
