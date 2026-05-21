from core.evidence.recursive_confidence_decay_engine import apply_recursive_confidence_decay


def test_depth_decays_confidence():
    low = apply_recursive_confidence_decay(0.7, {"level": "low", "confidence_limits": {"max_score": 0.9}}, depth=0)
    high = apply_recursive_confidence_decay(0.7, {"level": "low", "confidence_limits": {"max_score": 0.9}}, depth=4)
    assert high["score"] <= low["score"]
