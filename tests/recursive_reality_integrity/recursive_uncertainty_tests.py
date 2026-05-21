from core.evidence import structure_cognition


def test_recursive_uncertainty_preserved():
    r = structure_cognition({"a": 1}, {}, {"a": 1}, ambiguities=["u"])
    assert r["recursive_uncertainty"]["collapse_suppressed"] is True
