from core.evidence.semantic_hierarchy_engine import detect_semantic_hierarchy_permanence


def test_hierarchy_blocked():
    h = detect_semantic_hierarchy_permanence(4, True)
    assert h["suppress"] is True
