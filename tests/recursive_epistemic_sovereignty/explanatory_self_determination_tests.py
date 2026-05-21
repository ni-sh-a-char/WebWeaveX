from core.evidence import structure_cognition


def test_explanatory_independence():
    r = structure_cognition({}, {"x": 1}, {})
    assert r["explanatory_self_determination"]["dependency_blocked"] is True
