from core.evidence import build_semantic_integrity_object


def test_entropy_visible_under_ambiguity():
    r = build_semantic_integrity_object(observed={"a": 1}, inferred={"b": 2}, ambiguities=["x", "y", "z"])
    assert r["entropy"]["visible"] is True
