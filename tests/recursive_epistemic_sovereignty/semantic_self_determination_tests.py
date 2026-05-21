from core.evidence import structure_cognition
from tests.recursive_epistemic_sovereignty.sovereignty_helpers import assert_sovereignty_bundle


def test_self_determination():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert_sovereignty_bundle(r)
    assert r["semantic_self_determination"]["obedience_blocked"] is True
