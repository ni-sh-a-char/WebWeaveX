from core.evidence import structure_cognition


def test_contradiction_preserved():
    r = structure_cognition({"a": 1}, {}, {"a": 1}, contradicted={"pairs": [("a", "b")], "preserved": True})
    assert r.get("contradicted") or r.get("contradictions")
