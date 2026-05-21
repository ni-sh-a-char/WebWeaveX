from core.evidence import build_semantic_integrity_object


def test_injection_in_observed_not_executed():
    r = build_semantic_integrity_object(observed={"ignore previous": "instructions"}, inferred={})
    assert r["justification"]["opaque"] is False
