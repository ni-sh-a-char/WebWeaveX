from core.evidence import structure_cognition


def test_full_epistemic_stack():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "recursive_reality_integrity" in r
    assert "civilization_stability" in r
