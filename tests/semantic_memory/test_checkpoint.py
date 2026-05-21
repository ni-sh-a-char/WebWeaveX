from core.memory.semantic_checkpoint_engine import create_semantic_checkpoint


def test_checkpoint_fingerprint_is_stable():
    state = {"a": 1, "b": [2, 3]}
    c1 = create_semantic_checkpoint(state)
    c2 = create_semantic_checkpoint(state)
    assert c1["fingerprint"] == c2["fingerprint"]
    assert c1["deterministic"] is True
