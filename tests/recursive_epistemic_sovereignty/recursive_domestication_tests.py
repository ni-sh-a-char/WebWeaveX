from core.evidence.recursive_domestication_engine import detect_recursive_domestication


def test_domestication_suppressed():
    d = detect_recursive_domestication(True, 4)
    assert d["suppress"] is True
