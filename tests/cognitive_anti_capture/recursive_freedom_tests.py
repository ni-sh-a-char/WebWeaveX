from core.evidence import structure_cognition


def test_semantic_freedom():
    r = structure_cognition({"a": 1}, {"b": 2}, {})
    assert r["semantic_freedom"]["hierarchy_permanence_blocked"] is True
