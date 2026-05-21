from core.evidence.recursive_semantic_independence_engine import model_recursive_semantic_independence


def test_independence():
    i = model_recursive_semantic_independence(["a", "b"], 1)
    assert i["independent"] is True
