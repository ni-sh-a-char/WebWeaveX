from core.evidence import structure_cognition


def test_interpretive_agency():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["interpretive_self_determination"]["steering_blocked"] is True
