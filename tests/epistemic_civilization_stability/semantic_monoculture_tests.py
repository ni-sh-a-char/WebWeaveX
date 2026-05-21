from core.evidence.semantic_monoculture_engine import detect_semantic_monoculture


def test_monoculture_detected_at_depth():
    m = detect_semantic_monoculture([{"id": "only"}], [], 3)
    assert m["detected"] is True
