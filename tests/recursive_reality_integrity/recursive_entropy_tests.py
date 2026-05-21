from core.evidence.recursive_entropy_engine import model_recursive_entropy


def test_entropy_increases_with_depth():
    e1 = model_recursive_entropy(["a"], [], {}, 1)
    e3 = model_recursive_entropy(["a"], [], {}, 3)
    assert e3["entropy"] >= e1["entropy"]
    assert e3["preserved"] is True
