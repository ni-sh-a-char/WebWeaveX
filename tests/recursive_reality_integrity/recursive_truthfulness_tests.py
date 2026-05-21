from core.evidence import structure_cognition


def test_truth_preservation_chain():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "truth_preservation" in r
    assert "recursive_reality_integrity" in r
