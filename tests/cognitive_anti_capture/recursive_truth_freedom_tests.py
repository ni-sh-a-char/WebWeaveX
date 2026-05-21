from core.evidence import structure_cognition


def test_truth_and_freedom():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "truth_preservation" in r
    assert r["explanatory_freedom"]["monopolization_blocked"] is True
