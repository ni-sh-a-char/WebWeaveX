from core.identity import build_browser_identity, compute_runtime_entropy


def test_entropy_detection():
    baseline = build_browser_identity("default")
    stable = compute_runtime_entropy(baseline)

    drifted = build_browser_identity("profile_a")
    drift = compute_runtime_entropy(baseline, drifted)

    assert stable["stable"] is True
    assert stable["entropy_score"] == 0.0
    assert drift["stable"] is False
    assert drift["entropy_score"] == 1.0
