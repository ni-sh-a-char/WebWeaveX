from core.evidence.semantic_decay_engine import model_semantic_decay


def test_decay_without_evidence():
    d = model_semantic_decay([], {"x": 1}, 1)
    assert d["destabilize_unsupported"] is True
