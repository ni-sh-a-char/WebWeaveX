from core.evidence.semantic_orthodoxy_engine import detect_semantic_orthodoxy


def test_orthodoxy_at_depth():
    o = detect_semantic_orthodoxy([{"id": "one"}], 4)
    assert o["suppress"] is True
