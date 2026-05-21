from core.evidence import structure_cognition


def test_explanatory_alternatives():
    r = structure_cognition({}, {"x": 1, "y": 2}, {})
    assert r["explanatory_diversity"]["collapse_suppressed"] is True
