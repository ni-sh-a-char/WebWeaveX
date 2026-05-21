from core.evidence.recursive_obedience_engine import detect_recursive_obedience


def test_obedience_suppressed():
    o = detect_recursive_obedience(True, True, 3)
    assert o["suppress"] is True
