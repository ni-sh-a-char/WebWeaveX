from core.evidence import structure_cognition


def test_epistemic_layers_preserved():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert "civilizational_openness" in r
    assert "justification" in r
