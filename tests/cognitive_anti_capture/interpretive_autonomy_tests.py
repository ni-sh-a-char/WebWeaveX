from core.evidence import structure_cognition


def test_interpretive_autonomy():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["interpretive_autonomy"]["canonical_narrative_blocked"] is True
