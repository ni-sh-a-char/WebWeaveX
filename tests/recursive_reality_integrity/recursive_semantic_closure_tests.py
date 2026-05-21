from core.evidence.recursive_semantic_closure_engine import detect_recursive_semantic_closure


def test_closure_at_depth():
    c = detect_recursive_semantic_closure(3, {"a": 1, "b": 2}, {"a": 1, "b": 2}, [])
    assert c["closure_detected"] is True
