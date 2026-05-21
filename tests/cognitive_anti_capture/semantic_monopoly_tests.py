from core.evidence.semantic_monopoly_engine import detect_semantic_monopoly


def test_monopoly_suppressed():
    m = detect_semantic_monopoly(1, 3, 0)
    assert m["monopoly"] is True
    assert m["suppressed"]
