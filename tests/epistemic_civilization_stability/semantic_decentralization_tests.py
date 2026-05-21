from core.evidence import structure_cognition


def test_decentralization():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert r["semantic_decentralization"]["hierarchy_lock_in"] is False
