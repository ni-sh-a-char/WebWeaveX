from core.evidence import structure_cognition


def test_recursive_lineage():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert r.get("recursive_lineage", {}).get("decay_prevented") is True
