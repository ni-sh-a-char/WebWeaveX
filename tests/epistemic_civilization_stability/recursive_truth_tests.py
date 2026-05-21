from core.evidence import structure_cognition


def test_truth_and_openness():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "truth_preservation" in r
    assert r["epistemic_openness"]["anti_dogmatism"] is True
