from core.evidence import structure_cognition


def test_plurality_preserved():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["semantic_plurality"]["preserved"] is True
