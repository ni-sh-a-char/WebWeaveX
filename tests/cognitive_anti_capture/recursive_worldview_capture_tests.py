from core.evidence import structure_cognition


def test_worldview_capture():
    r = structure_cognition({"a": 1}, {"b": 2}, {}, contradicted={"pairs": [("a", "b")]})
    assert r["worldview_diversity"]["convergence_suppressed"] is True
