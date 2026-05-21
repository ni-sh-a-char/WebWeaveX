from core.persistence import persist_semantic_ir


def test_persist_fingerprint_stable():
    ir = {"nodes": [{"id": "a"}]}
    a = persist_semantic_ir(ir)
    b = persist_semantic_ir(ir)
    assert a["fingerprint"] == b["fingerprint"]
    assert a["persisted"] is True
