from core.evidence.recursive_narrative_monopoly_engine import detect_recursive_narrative_monopoly


def test_narrative_monopoly():
    n = detect_recursive_narrative_monopoly(1, 3)
    assert n["suppress"] is True
