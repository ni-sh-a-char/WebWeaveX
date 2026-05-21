from core.evidence import structure_cognition


def test_full_stack():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert "cognitive_anti_capture" in r
    assert "epistemic_sovereignty" in r
