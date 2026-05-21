from core.internet.probabilistic_trust_engine import compute_probabilistic_trust
from core.internet.trust_error_analysis_engine import analyze_trust_error


def test_probabilistic_trust_deterministic():
    a = compute_probabilistic_trust("https://docs.python.org/3/", corroboration_count=2)
    b = compute_probabilistic_trust("https://docs.python.org/3/", corroboration_count=2)
    assert a["trust_score"] == b["trust_score"]
    assert a["calibrated"] is True


def test_trust_error_mae():
    r = analyze_trust_error([{"predicted": 0.8, "actual": 0.7}, {"predicted": 0.5, "actual": 0.6}])
    assert r["mean_absolute_error"] > 0
