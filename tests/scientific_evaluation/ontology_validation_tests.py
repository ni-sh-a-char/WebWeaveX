from core.knowledge.semantic_merge_validator import validate_semantic_merge


def test_merge_blocked_on_conflict_pressure():
    r = validate_semantic_merge(
        [{"evidence": ["a"]}],
        [{"from": "a", "to": "b", "contradictions": {"pairs": [["x", "y"]] * 5}}],
    )
    assert r["allowed"] is False
