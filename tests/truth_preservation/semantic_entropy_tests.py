from core.evidence.semantic_entropy_engine import model_semantic_entropy


def test_entropy_preserved():
    e = model_semantic_entropy(["a"], ["u"], {"pairs": [("x", "y")]})
    assert e["preserved"] is True
    assert e["entropy"] > 0
