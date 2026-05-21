from core.evidence import structure_cognition


def test_ambiguity_not_collapsed():
    r = structure_cognition({}, {}, {}, ambiguities=["term"])
    assert "term" in r.get("ambiguities", [])
