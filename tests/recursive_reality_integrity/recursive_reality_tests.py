from core.evidence import structure_cognition
from tests.recursive_reality_integrity.recursive_helpers import assert_recursive_bundle


def test_recursive_bundle():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert_recursive_bundle(r)
