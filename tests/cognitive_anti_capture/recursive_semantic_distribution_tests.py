from core.evidence.recursive_semantic_distribution_engine import distribute_recursive_semantics


def test_distribution():
    d = distribute_recursive_semantics(["a", "b", "c"])
    assert d["distributed"] is True
