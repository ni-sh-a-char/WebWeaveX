from core.evidence import structure_cognition


def test_truth_without_dependency():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "truth_preservation" in r
    assert r["epistemic_sovereignty"]["preserved"] is True
