from core.evidence import structure_cognition


def test_uncertainty_visible():
    r = structure_cognition({"a": 1}, {}, {"a": 1}, ambiguities=["u"])
    assert r["uncertainty_visibility"]["preserved"] is True
