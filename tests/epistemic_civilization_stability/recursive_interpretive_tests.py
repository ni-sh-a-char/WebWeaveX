from core.evidence.interpretive_closure_engine import detect_interpretive_closure


def test_closure_suppressed():
    c = detect_interpretive_closure(1, 3)
    assert c["suppress"] is True
