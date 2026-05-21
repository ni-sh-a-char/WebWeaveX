from core.evidence import structure_cognition


def test_semantic_diversity():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["semantic_diversity"]["preserved"] is True
