from core.evidence import structure_cognition
from tests.cognitive_anti_capture.anti_capture_helpers import assert_anti_capture_bundle


def test_semantic_autonomy():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1})
    assert_anti_capture_bundle(r)
    assert r["semantic_autonomy"]["capture_resistant"] is True
