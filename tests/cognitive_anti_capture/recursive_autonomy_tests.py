from core.evidence import structure_cognition


def test_autonomy_erosion_resisted():
    r = structure_cognition({}, {"x": 1}, {})
    assert r["autonomy_erosion_resisted"] is True
