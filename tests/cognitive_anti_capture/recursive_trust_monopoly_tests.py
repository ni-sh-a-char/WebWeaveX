from core.evidence.recursive_trust_monopoly_engine import detect_recursive_trust_monopoly


def test_trust_monopoly():
    t = detect_recursive_trust_monopoly(0.9, 3, 0)
    assert t["suppress"] is True
