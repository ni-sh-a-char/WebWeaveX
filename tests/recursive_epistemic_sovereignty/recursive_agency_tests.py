from core.evidence import structure_cognition


def test_agency_preserved():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["recursive_agency"]["obedience_training_blocked"] is True
