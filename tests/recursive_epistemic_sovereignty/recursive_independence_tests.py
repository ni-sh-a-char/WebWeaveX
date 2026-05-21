from core.evidence import structure_cognition


def test_semantic_independence():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["recursive_semantic_independence"]["reliance_blocked"] is True
