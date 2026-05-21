from core.evidence.semantic_consistency_engine import assess_semantic_consistency


def test_consistent_reconciliation():
    r = assess_semantic_consistency({"a": 1}, {"b": 2}, {"a": 1})
    assert "consistency_score" in r
