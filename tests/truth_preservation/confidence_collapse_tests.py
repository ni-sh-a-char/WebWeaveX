from core.evidence.confidence_collapse_engine import apply_confidence_collapse


def test_collapse_reduces_score():
    c = apply_confidence_collapse(0.8, {"level": "low", "confidence_limits": {"max_score": 0.9}}, stabilization_count=2)
    assert c["score"] < 0.8
    assert c.get("collapse_pressure")
