from core.evidence import structure_cognition


def test_ambiguity_not_suppressed():
    r = structure_cognition({}, {}, {}, ambiguities=["term"])
    assert "term" in r.get("ambiguities", [])
    assert r["ambiguity_visibility"]["preserved"] is True
