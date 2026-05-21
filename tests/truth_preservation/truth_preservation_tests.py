from core.evidence import structure_cognition
from tests.truth_preservation.truth_helpers import assert_truth_bundle


def test_truth_bundle():
    r = structure_cognition({"a": 1}, {}, {"a": 1})
    assert_truth_bundle(r)
