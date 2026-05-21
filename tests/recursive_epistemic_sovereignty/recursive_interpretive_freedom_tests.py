from core.evidence import structure_cognition


def test_interpretive_independence():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["recursive_interpretive_independence"]["collapse_blocked"] is True
