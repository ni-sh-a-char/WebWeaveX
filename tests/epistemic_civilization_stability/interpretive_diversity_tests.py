from core.evidence import structure_cognition


def test_multiple_interpretations():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert r["interpretive_diversity"]["count"] >= 1
