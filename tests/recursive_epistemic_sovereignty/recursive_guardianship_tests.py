from core.evidence.recursive_guardianship_engine import detect_recursive_guardianship


def test_guardianship_blocked():
    g = detect_recursive_guardianship(True, 3)
    assert g["suppress"] is True
