from core.evidence import structure_cognition


def test_worldview_not_dependent():
    r = structure_cognition({"a": 1}, {"b": 2}, {}, contradicted={"pairs": [("a", "b")]})
    assert r["worldview_diversity"]["diverse"] is True
