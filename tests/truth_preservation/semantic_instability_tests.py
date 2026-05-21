from core.evidence import structure_cognition


def test_instability_preserved():
    r = structure_cognition({}, {"x": 1}, {})
    assert r["instability"].get("preserved") or r["semantic_instability"].get("preserved")
